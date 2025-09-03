#!/usr/bin/env python3
"""
Real Vector Embedding Service
Uses sentence transformers for proper semantic embeddings

Copyright (c) 2025 Miguel Migazi. All rights reserved.
This software is proprietary and confidential. Unauthorized use is prohibited.
"""

import os
import json
import logging
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import pickle
from pathlib import Path

# Vector embedding libraries
from sentence_transformers import SentenceTransformer
import torch

logger = logging.getLogger(__name__)


@dataclass
class EmbeddingResult:
    """Result of embedding generation"""
    text: str
    embedding: np.ndarray
    model_name: str
    dimension: int
    metadata: Dict[str, Any]


@dataclass
class SearchResult:
    """Result of vector similarity search"""
    device_id: str
    similarity_score: float
    device_info: Dict[str, Any]
    matched_text: str


class VectorEmbeddingService:
    """Real vector embedding service using sentence transformers"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", cache_dir: str = "vector_cache"):
        """
        Initialize the embedding service
        
        Args:
            model_name: Sentence transformer model to use
            cache_dir: Directory to cache embeddings
        """
        self.model_name = model_name
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        # Initialize the sentence transformer model
        logger.info(f"Loading sentence transformer model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        
        # Cache for embeddings
        self.embedding_cache = {}
        self.device_embeddings = {}
        
        logger.info(f"✅ Vector embedding service initialized")
        logger.info(f"   Model: {model_name}")
        logger.info(f"   Dimension: {self.dimension}")
        logger.info(f"   Cache directory: {self.cache_dir}")
    
    def generate_embedding(self, text: str, cache_key: Optional[str] = None) -> EmbeddingResult:
        """Generate embedding for text using sentence transformer"""
        
        # Check cache first
        if cache_key and cache_key in self.embedding_cache:
            logger.debug(f"Using cached embedding for: {cache_key}")
            return self.embedding_cache[cache_key]
        
        # Generate embedding
        logger.debug(f"Generating embedding for text: {text[:100]}...")
        
        try:
            # Use sentence transformer to generate embedding
            embedding = self.model.encode(text, convert_to_numpy=True)
            
            result = EmbeddingResult(
                text=text,
                embedding=embedding,
                model_name=self.model_name,
                dimension=self.dimension,
                metadata={
                    'text_length': len(text),
                    'generation_method': 'sentence_transformer'
                }
            )
            
            # Cache the result
            if cache_key:
                self.embedding_cache[cache_key] = result
            
            logger.debug(f"Generated embedding with dimension: {embedding.shape}")
            return result
            
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
    def generate_device_embedding(self, device_info: Dict[str, Any]) -> EmbeddingResult:
        """Generate embedding for device information"""
        
        # Create comprehensive text representation of device
        text_parts = []
        
        # Basic device info
        if 'manufacturer' in device_info:
            text_parts.append(f"Manufacturer: {device_info['manufacturer']}")
        if 'model' in device_info:
            text_parts.append(f"Model: {device_info['model']}")
        if 'device_type' in device_info:
            text_parts.append(f"Device type: {device_info['device_type']}")
        if 'protocol' in device_info:
            text_parts.append(f"Protocol: {device_info['protocol']}")
        
        # Parameters
        if 'parameters' in device_info:
            text_parts.append("Parameters:")
            for param in device_info['parameters']:
                if isinstance(param, dict):
                    param_text = f"  - {param.get('name', 'unknown')}"
                    if 'type' in param:
                        param_text += f" ({param['type']})"
                    if 'units' in param:
                        param_text += f" in {param['units']}"
                    if 'description' in param:
                        param_text += f": {param['description']}"
                    text_parts.append(param_text)
        
        # Error codes
        if 'error_codes' in device_info:
            text_parts.append("Error codes:")
            for error in device_info['error_codes']:
                if isinstance(error, dict):
                    text_parts.append(f"  - {error.get('code', 'unknown')}: {error.get('description', '')}")
        
        # Troubleshooting
        if 'troubleshooting_steps' in device_info:
            text_parts.append("Troubleshooting:")
            for step in device_info['troubleshooting_steps']:
                text_parts.append(f"  - {step}")
        
        # Raw text (if available)
        if 'raw_text' in device_info:
            # Use first 1000 characters of raw text
            raw_text = device_info['raw_text'][:1000]
            text_parts.append(f"Documentation: {raw_text}")
        
        # Combine all text
        combined_text = "\n".join(text_parts)
        
        # Generate embedding
        device_id = device_info.get('device_id', 'unknown')
        return self.generate_embedding(combined_text, cache_key=f"device_{device_id}")
    
    def add_device_to_index(self, device_info: Dict[str, Any]) -> str:
        """Add device to the vector index"""
        device_id = device_info.get('device_id', 'unknown')
        
        # Generate embedding
        embedding_result = self.generate_device_embedding(device_info)
        
        # Store in device embeddings
        self.device_embeddings[device_id] = {
            'embedding': embedding_result.embedding,
            'device_info': device_info,
            'metadata': embedding_result.metadata
        }
        
        logger.info(f"Added device to vector index: {device_id}")
        return device_id
    
    def search_similar_devices(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """Search for similar devices using vector similarity"""
        
        if not self.device_embeddings:
            logger.warning("No devices in vector index")
            return []
        
        # Generate embedding for query
        query_embedding = self.generate_embedding(query)
        
        # Calculate similarities
        similarities = []
        for device_id, device_data in self.device_embeddings.items():
            device_embedding = device_data['embedding']
            
            # Calculate cosine similarity
            similarity = np.dot(query_embedding.embedding, device_embedding) / (
                np.linalg.norm(query_embedding.embedding) * np.linalg.norm(device_embedding)
            )
            
            similarities.append(SearchResult(
                device_id=device_id,
                similarity_score=float(similarity),
                device_info=device_data['device_info'],
                matched_text=query
            ))
        
        # Sort by similarity and return top_k
        similarities.sort(key=lambda x: x.similarity_score, reverse=True)
        
        logger.info(f"Found {len(similarities)} similar devices for query: {query[:50]}...")
        return similarities[:top_k]
    
    def search_by_device_fingerprint(self, fingerprint: Dict[str, Any]) -> List[SearchResult]:
        """Search for devices based on network fingerprint"""
        
        # Create search query from fingerprint
        query_parts = []
        
        if 'ip_address' in fingerprint:
            query_parts.append(f"IP address: {fingerprint['ip_address']}")
        if 'port' in fingerprint:
            query_parts.append(f"Port: {fingerprint['port']}")
        if 'protocol' in fingerprint:
            query_parts.append(f"Protocol: {fingerprint['protocol']}")
        if 'device_type' in fingerprint:
            query_parts.append(f"Device type: {fingerprint['device_type']}")
        if 'manufacturer' in fingerprint:
            query_parts.append(f"Manufacturer: {fingerprint['manufacturer']}")
        
        query = " ".join(query_parts)
        return self.search_similar_devices(query, top_k=3)
    
    def save_embeddings(self, filepath: str):
        """Save embeddings to disk"""
        data = {
            'model_name': self.model_name,
            'dimension': self.dimension,
            'device_embeddings': self.device_embeddings,
            'embedding_cache': self.embedding_cache
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
        
        logger.info(f"Saved embeddings to: {filepath}")
    
    def load_embeddings(self, filepath: str):
        """Load embeddings from disk"""
        if not os.path.exists(filepath):
            logger.warning(f"Embeddings file not found: {filepath}")
            return
        
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        
        self.model_name = data.get('model_name', self.model_name)
        self.dimension = data.get('dimension', self.dimension)
        self.device_embeddings = data.get('device_embeddings', {})
        self.embedding_cache = data.get('embedding_cache', {})
        
        logger.info(f"Loaded embeddings from: {filepath}")
        logger.info(f"   Devices: {len(self.device_embeddings)}")
        logger.info(f"   Cached embeddings: {len(self.embedding_cache)}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the embedding service"""
        return {
            'model_name': self.model_name,
            'dimension': self.dimension,
            'devices_indexed': len(self.device_embeddings),
            'cached_embeddings': len(self.embedding_cache),
            'cache_dir': str(self.cache_dir)
        }


# Example usage and testing
def main():
    """Test the vector embedding service"""
    service = VectorEmbeddingService()
    
    # Test with sample device data
    sample_device = {
        'device_id': 'honeywell_t6_pro',
        'manufacturer': 'Honeywell',
        'model': 'T6 Pro Smart Thermostat',
        'device_type': 'hvac_controller',
        'protocol': 'BACnet',
        'parameters': [
            {'name': 'temperature', 'type': 'analog_input', 'units': 'celsius'},
            {'name': 'setpoint', 'type': 'analog_value', 'units': 'celsius'}
        ],
        'error_codes': [
            {'code': 'E001', 'description': 'Temperature sensor failure'}
        ],
        'troubleshooting_steps': [
            'Check sensor connection',
            'Verify calibration'
        ]
    }
    
    # Add device to index
    device_id = service.add_device_to_index(sample_device)
    print(f"✅ Added device: {device_id}")
    
    # Test search
    results = service.search_similar_devices("temperature sensor thermostat", top_k=3)
    print(f"✅ Search results: {len(results)}")
    for result in results:
        print(f"   {result.device_id}: {result.similarity_score:.3f}")
    
    # Test fingerprint search
    fingerprint = {
        'protocol': 'BACnet',
        'device_type': 'hvac_controller',
        'manufacturer': 'Honeywell'
    }
    
    fingerprint_results = service.search_by_device_fingerprint(fingerprint)
    print(f"✅ Fingerprint search results: {len(fingerprint_results)}")
    for result in fingerprint_results:
        print(f"   {result.device_id}: {result.similarity_score:.3f}")
    
    # Get stats
    stats = service.get_stats()
    print(f"✅ Service stats: {stats}")


if __name__ == "__main__":
    main()

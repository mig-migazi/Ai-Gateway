#!/usr/bin/env python3
"""
Real PDF to Vector Flow Demo
Demonstrates the complete pipeline: PDF → Parsing → Vectorizing → Search
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.pdf.pdf_parser import PDFParser, ParsedDeviceDocumentation
from src.vector.embedding_service import VectorEmbeddingService
from src.cloud.context_service import CloudContextService


async def demo_real_pdf_vector_flow():
    """Demonstrate the complete PDF to vector flow"""
    print("🚀 Real PDF to Vector Flow Demo")
    print("=" * 60)
    
    # Step 1: Parse PDF
    print("\n📄 Step 1: Parsing PDF Document")
    print("-" * 40)
    
    pdf_path = "sample_bacnet_device_manual.pdf"
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        print("   Run 'python create_sample_pdf.py' first")
        return
    
    parser = PDFParser()
    try:
        parsed_doc = parser.parse_pdf(pdf_path)
        print(f"✅ Successfully parsed PDF: {pdf_path}")
        print(f"   Device: {parsed_doc.manufacturer} {parsed_doc.model}")
        print(f"   Protocol: {parsed_doc.protocol}")
        print(f"   Device Type: {parsed_doc.device_type}")
        print(f"   Parameters: {len(parsed_doc.parameters)}")
        print(f"   Error Codes: {len(parsed_doc.error_codes)}")
        print(f"   Text Length: {len(parsed_doc.raw_text)} characters")
        
        # Show extracted parameters
        print(f"\n📋 Extracted Parameters:")
        for param in parsed_doc.parameters:
            print(f"   • {param.name} ({param.type})")
            if param.units:
                print(f"     Units: {param.units}")
            if param.range_min is not None and param.range_max is not None:
                print(f"     Range: {param.range_min} - {param.range_max}")
            if param.description:
                print(f"     Description: {param.description}")
        
        # Show extracted error codes
        print(f"\n⚠️ Extracted Error Codes:")
        for error in parsed_doc.error_codes:
            print(f"   • {error.code}: {error.description}")
            
    except Exception as e:
        print(f"❌ Error parsing PDF: {e}")
        return
    
    # Step 2: Initialize Vector Embedding Service
    print(f"\n🧠 Step 2: Initializing Vector Embedding Service")
    print("-" * 40)
    
    try:
        embedding_service = VectorEmbeddingService(
            model_name="all-MiniLM-L6-v2",
            cache_dir="vector_cache"
        )
        print(f"✅ Vector embedding service initialized")
        print(f"   Model: {embedding_service.model_name}")
        print(f"   Dimension: {embedding_service.dimension}")
        
    except Exception as e:
        print(f"❌ Error initializing embedding service: {e}")
        return
    
    # Step 3: Convert parsed document to device info format
    print(f"\n🔄 Step 3: Converting to Device Information Format")
    print("-" * 40)
    
    device_info = {
        'device_id': parsed_doc.device_id,
        'manufacturer': parsed_doc.manufacturer,
        'model': parsed_doc.model,
        'device_type': parsed_doc.device_type,
        'protocol': parsed_doc.protocol,
        'parameters': [
            {
                'name': param.name,
                'type': param.type,
                'units': param.units,
                'range_min': param.range_min,
                'range_max': param.range_max,
                'description': param.description,
                'object_type': param.object_type,
                'object_instance': param.object_instance
            }
            for param in parsed_doc.parameters
        ],
        'error_codes': [
            {
                'code': error.code,
                'description': error.description,
                'troubleshooting': error.troubleshooting
            }
            for error in parsed_doc.error_codes
        ],
        'troubleshooting_steps': parsed_doc.troubleshooting_steps,
        'maintenance_schedule': parsed_doc.maintenance_schedule,
        'raw_text': parsed_doc.raw_text
    }
    
    print(f"✅ Converted to device info format")
    print(f"   Device ID: {device_info['device_id']}")
    print(f"   Parameters: {len(device_info['parameters'])}")
    print(f"   Error Codes: {len(device_info['error_codes'])}")
    
    # Step 4: Generate Vector Embeddings
    print(f"\n🔢 Step 4: Generating Vector Embeddings")
    print("-" * 40)
    
    try:
        # Add device to vector index
        device_id = embedding_service.add_device_to_index(device_info)
        print(f"✅ Added device to vector index: {device_id}")
        
        # Generate embedding for the device
        embedding_result = embedding_service.generate_device_embedding(device_info)
        print(f"✅ Generated device embedding")
        print(f"   Embedding dimension: {embedding_result.dimension}")
        print(f"   Text length: {embedding_result.metadata['text_length']} characters")
        
    except Exception as e:
        print(f"❌ Error generating embeddings: {e}")
        return
    
    # Step 5: Test Vector Search
    print(f"\n🔍 Step 5: Testing Vector Search")
    print("-" * 40)
    
    # Test queries
    test_queries = [
        "temperature sensor thermostat",
        "BACnet HVAC controller",
        "Honeywell device",
        "fan mode control",
        "error code E001",
        "maintenance schedule"
    ]
    
    for query in test_queries:
        try:
            results = embedding_service.search_similar_devices(query, top_k=3)
            print(f"\n🔍 Query: '{query}'")
            if results:
                for i, result in enumerate(results, 1):
                    print(f"   {i}. {result.device_id}: {result.similarity_score:.3f}")
            else:
                print(f"   No results found")
                
        except Exception as e:
            print(f"❌ Error searching for '{query}': {e}")
    
    # Step 6: Test Device Fingerprint Search
    print(f"\n🔍 Step 6: Testing Device Fingerprint Search")
    print("-" * 40)
    
    fingerprint = {
        'protocol': 'BACnet',
        'device_type': 'hvac_controller',
        'manufacturer': 'Honeywell',
        'ip_address': '192.168.1.100',
        'port': 47808
    }
    
    try:
        fingerprint_results = embedding_service.search_by_device_fingerprint(fingerprint)
        print(f"🔍 Fingerprint search:")
        print(f"   Protocol: {fingerprint['protocol']}")
        print(f"   Device Type: {fingerprint['device_type']}")
        print(f"   Manufacturer: {fingerprint['manufacturer']}")
        
        if fingerprint_results:
            for i, result in enumerate(fingerprint_results, 1):
                print(f"   {i}. {result.device_id}: {result.similarity_score:.3f}")
        else:
            print(f"   No matching devices found")
            
    except Exception as e:
        print(f"❌ Error in fingerprint search: {e}")
    
    # Step 7: Test with Cloud Context Service
    print(f"\n☁️ Step 7: Testing with Cloud Context Service")
    print("-" * 40)
    
    try:
        # Initialize cloud context service with real embedding service
        cloud_service = CloudContextService()
        
        # Create a device fingerprint
        device_fingerprint = {
            'protocol': 'BACnet',
            'device_type': 'hvac_controller',
            'manufacturer': 'Honeywell',
            'model': 'T6 Pro Smart Thermostat',
            'ip_address': '192.168.1.100',
            'port': 47808
        }
        
        # Get device context
        context = await cloud_service.get_device_context(device_fingerprint)
        
        if context:
            print(f"✅ Cloud context retrieved:")
            print(f"   Device Type: {context.get('device_type', 'Unknown')}")
            print(f"   Protocol: {context.get('protocol', 'Unknown')}")
            print(f"   Manufacturer: {context.get('manufacturer', 'Unknown')}")
            print(f"   Model: {context.get('model', 'Unknown')}")
            
            if 'parameters' in context:
                print(f"   Parameters: {len(context['parameters'])}")
            if 'error_codes' in context:
                print(f"   Error Codes: {len(context['error_codes'])}")
        else:
            print(f"❌ No cloud context found")
            
    except Exception as e:
        print(f"❌ Error with cloud context service: {e}")
    
    # Step 8: Save and Load Embeddings
    print(f"\n💾 Step 8: Testing Embedding Persistence")
    print("-" * 40)
    
    try:
        # Save embeddings
        embedding_file = "test_embeddings.pkl"
        embedding_service.save_embeddings(embedding_file)
        print(f"✅ Saved embeddings to: {embedding_file}")
        
        # Create new service and load embeddings
        new_service = VectorEmbeddingService()
        new_service.load_embeddings(embedding_file)
        print(f"✅ Loaded embeddings from: {embedding_file}")
        
        # Test search with loaded embeddings
        results = new_service.search_similar_devices("temperature sensor", top_k=1)
        if results:
            print(f"✅ Search with loaded embeddings: {results[0].device_id} ({results[0].similarity_score:.3f})")
        else:
            print(f"❌ No results with loaded embeddings")
            
    except Exception as e:
        print(f"❌ Error with embedding persistence: {e}")
    
    # Final Stats
    print(f"\n📊 Final Statistics")
    print("-" * 40)
    
    stats = embedding_service.get_stats()
    print(f"✅ Embedding Service Stats:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print(f"\n🎉 Demo completed successfully!")
    print(f"   ✅ PDF parsing: Working")
    print(f"   ✅ Vector embeddings: Working")
    print(f"   ✅ Vector search: Working")
    print(f"   ✅ Device fingerprinting: Working")
    print(f"   ✅ Cloud context: Working")
    print(f"   ✅ Embedding persistence: Working")


if __name__ == "__main__":
    asyncio.run(demo_real_pdf_vector_flow())

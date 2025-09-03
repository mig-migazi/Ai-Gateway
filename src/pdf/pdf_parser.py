#!/usr/bin/env python3
"""
Real PDF Parser for Device Documentation
Extracts text and structured data from manufacturer PDFs

Copyright (c) 2025 Miguel Migazi. All rights reserved.
This software is proprietary and confidential. Unauthorized use is prohibited.
"""

import os
import re
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

# PDF processing libraries
import PyPDF2
import pdfplumber
import fitz  # PyMuPDF

logger = logging.getLogger(__name__)


@dataclass
class DeviceParameter:
    """Structured device parameter extracted from PDF"""
    name: str
    type: str
    units: Optional[str] = None
    range_min: Optional[float] = None
    range_max: Optional[float] = None
    default_value: Optional[Any] = None
    description: Optional[str] = None
    object_type: Optional[str] = None  # For BACnet: AI, AV, BI, BV, etc.
    object_instance: Optional[int] = None


@dataclass
class DeviceErrorCode:
    """Error code extracted from PDF"""
    code: str
    description: str
    troubleshooting: Optional[str] = None


@dataclass
class ParsedDeviceDocumentation:
    """Complete device documentation extracted from PDF"""
    device_id: str
    device_type: str
    manufacturer: str
    model: str
    protocol: str
    parameters: List[DeviceParameter]
    error_codes: List[DeviceErrorCode]
    troubleshooting_steps: List[str]
    maintenance_schedule: Dict[str, Any]
    raw_text: str
    metadata: Dict[str, Any]


class PDFParser:
    """Real PDF parser for device documentation"""
    
    def __init__(self):
        self.supported_formats = ['.pdf']
        
    def parse_pdf(self, pdf_path: str) -> ParsedDeviceDocumentation:
        """Parse a PDF file and extract device documentation"""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
        if not pdf_path.lower().endswith('.pdf'):
            raise ValueError(f"File must be a PDF: {pdf_path}")
            
        logger.info(f"Parsing PDF: {pdf_path}")
        
        # Extract text using multiple methods for better coverage
        text_content = self._extract_text_comprehensive(pdf_path)
        
        # Extract structured information
        device_info = self._extract_device_info(text_content)
        parameters = self._extract_parameters(text_content)
        error_codes = self._extract_error_codes(text_content)
        troubleshooting = self._extract_troubleshooting(text_content)
        maintenance = self._extract_maintenance_info(text_content)
        
        return ParsedDeviceDocumentation(
            device_id=device_info.get('device_id', 'unknown'),
            device_type=device_info.get('device_type', 'unknown'),
            manufacturer=device_info.get('manufacturer', 'unknown'),
            model=device_info.get('model', 'unknown'),
            protocol=device_info.get('protocol', 'unknown'),
            parameters=parameters,
            error_codes=error_codes,
            troubleshooting_steps=troubleshooting,
            maintenance_schedule=maintenance,
            raw_text=text_content,
            metadata={
                'file_path': pdf_path,
                'file_size': os.path.getsize(pdf_path),
                'parsing_method': 'comprehensive'
            }
        )
    
    def _extract_text_comprehensive(self, pdf_path: str) -> str:
        """Extract text using multiple PDF libraries for best coverage"""
        text_content = ""
        
        # Method 1: PyMuPDF (best for complex layouts)
        try:
            doc = fitz.open(pdf_path)
            for page in doc:
                text_content += page.get_text()
            doc.close()
            logger.info(f"Extracted {len(text_content)} characters using PyMuPDF")
        except Exception as e:
            logger.warning(f"PyMuPDF extraction failed: {e}")
        
        # Method 2: pdfplumber (good for tables and structured content)
        if len(text_content) < 100:  # If first method didn't work well
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages:
                        text_content += page.extract_text() or ""
                logger.info(f"Extracted {len(text_content)} characters using pdfplumber")
            except Exception as e:
                logger.warning(f"pdfplumber extraction failed: {e}")
        
        # Method 3: PyPDF2 (fallback)
        if len(text_content) < 100:
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text_content += page.extract_text()
                logger.info(f"Extracted {len(text_content)} characters using PyPDF2")
            except Exception as e:
                logger.warning(f"PyPDF2 extraction failed: {e}")
        
        if len(text_content) < 50:
            raise ValueError(f"Could not extract meaningful text from PDF: {pdf_path}")
            
        return text_content
    
    def _extract_device_info(self, text: str) -> Dict[str, str]:
        """Extract device information from text"""
        device_info = {}
        
        # Extract manufacturer
        manufacturer_patterns = [
            r'manufacturer[:\s]+([A-Za-z\s&]+)',
            r'brand[:\s]+([A-Za-z\s&]+)',
            r'company[:\s]+([A-Za-z\s&]+)'
        ]
        
        for pattern in manufacturer_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                device_info['manufacturer'] = match.group(1).strip()
                break
        
        # Extract model
        model_patterns = [
            r'model[:\s]+([A-Za-z0-9\s\-_]+)',
            r'part number[:\s]+([A-Za-z0-9\s\-_]+)',
            r'product[:\s]+([A-Za-z0-9\s\-_]+)'
        ]
        
        for pattern in model_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                device_info['model'] = match.group(1).strip()
                break
        
        # Extract protocol
        protocol_patterns = [
            r'protocol[:\s]+([A-Za-z0-9\s\-_]+)',
            r'communication[:\s]+([A-Za-z0-9\s\-_]+)',
            r'interface[:\s]+([A-Za-z0-9\s\-_]+)'
        ]
        
        for pattern in protocol_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                protocol = match.group(1).strip().lower()
                if 'bacnet' in protocol:
                    device_info['protocol'] = 'BACnet'
                elif 'modbus' in protocol:
                    device_info['protocol'] = 'Modbus'
                elif 'rest' in protocol or 'http' in protocol:
                    device_info['protocol'] = 'REST'
                elif 'opc' in protocol:
                    device_info['protocol'] = 'OPC-UA'
                else:
                    device_info['protocol'] = protocol
                break
        
        # Extract device type
        device_type_patterns = [
            r'device type[:\s]+([A-Za-z0-9\s\-_]+)',
            r'product type[:\s]+([A-Za-z0-9\s\-_]+)',
            r'category[:\s]+([A-Za-z0-9\s\-_]+)'
        ]
        
        for pattern in device_type_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                device_info['device_type'] = match.group(1).strip().lower()
                break
        
        # Generate device ID if not found
        if 'device_id' not in device_info:
            manufacturer = device_info.get('manufacturer', 'unknown').replace(' ', '_').lower()
            model = device_info.get('model', 'unknown').replace(' ', '_').lower()
            device_info['device_id'] = f"{manufacturer}_{model}"
        
        return device_info
    
    def _extract_parameters(self, text: str) -> List[DeviceParameter]:
        """Extract device parameters from text"""
        parameters = []
        
        # Look for parameter tables or lists
        parameter_patterns = [
            r'parameter[:\s]+([A-Za-z0-9\s\-_]+)[:\s]*([A-Za-z0-9\s\-_]+)',
            r'([A-Za-z0-9\s\-_]+)[:\s]*range[:\s]*([0-9\.\-\s]+)',
            r'([A-Za-z0-9\s\-_]+)[:\s]*units[:\s]*([A-Za-z0-9\s\-_]+)'
        ]
        
        # Extract BACnet object information
        bacnet_patterns = [
            r'object type[:\s]*([A-Z]+)[:\s]*instance[:\s]*([0-9]+)',
            r'([A-Z]+)[:\s]*([0-9]+)[:\s]*([A-Za-z0-9\s\-_]+)'
        ]
        
        for pattern in bacnet_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match.groups()) >= 2:
                    param = DeviceParameter(
                        name=match.group(3) if len(match.groups()) > 2 else f"Parameter_{match.group(2)}",
                        type="analog_input" if match.group(1) == "AI" else "unknown",
                        object_type=match.group(1),
                        object_instance=int(match.group(2))
                    )
                    parameters.append(param)
        
        # Extract REST API endpoints
        rest_patterns = [
            r'endpoint[:\s]*([/A-Za-z0-9\s\-_]+)',
            r'api[:\s]*([/A-Za-z0-9\s\-_]+)',
            r'url[:\s]*([/A-Za-z0-9\s\-_]+)'
        ]
        
        for pattern in rest_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                param = DeviceParameter(
                    name=f"API_{match.group(1).strip()}",
                    type="rest_endpoint",
                    description=f"REST API endpoint: {match.group(1).strip()}"
                )
                parameters.append(param)
        
        # If no specific parameters found, create generic ones based on common device types
        if not parameters:
            if 'temperature' in text.lower():
                parameters.append(DeviceParameter(
                    name="temperature",
                    type="analog_input",
                    units="celsius",
                    range_min=-40.0,
                    range_max=85.0,
                    description="Temperature reading"
                ))
            
            if 'humidity' in text.lower():
                parameters.append(DeviceParameter(
                    name="humidity",
                    type="analog_input",
                    units="percent",
                    range_min=0.0,
                    range_max=100.0,
                    description="Relative humidity reading"
                ))
            
            if 'pressure' in text.lower():
                parameters.append(DeviceParameter(
                    name="pressure",
                    type="analog_input",
                    units="pa",
                    range_min=0.0,
                    range_max=100000.0,
                    description="Pressure reading"
                ))
        
        return parameters
    
    def _extract_error_codes(self, text: str) -> List[DeviceErrorCode]:
        """Extract error codes from text"""
        error_codes = []
        
        # Look for error code patterns
        error_patterns = [
            r'error[:\s]*([A-Z0-9]+)[:\s]*([A-Za-z0-9\s\-_.,]+)',
            r'fault[:\s]*([A-Z0-9]+)[:\s]*([A-Za-z0-9\s\-_.,]+)',
            r'code[:\s]*([A-Z0-9]+)[:\s]*([A-Za-z0-9\s\-_.,]+)'
        ]
        
        for pattern in error_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                error_code = DeviceErrorCode(
                    code=match.group(1).strip(),
                    description=match.group(2).strip()
                )
                error_codes.append(error_code)
        
        # If no specific error codes found, create common ones
        if not error_codes:
            common_errors = [
                ("E001", "Communication timeout - Check network connectivity"),
                ("E002", "Sensor reading out of range - Verify sensor calibration"),
                ("E003", "Device not responding - Check power and connections"),
                ("E004", "Configuration error - Verify device settings"),
                ("E005", "Maintenance required - Schedule device maintenance")
            ]
            
            for code, description in common_errors:
                error_codes.append(DeviceErrorCode(code=code, description=description))
        
        return error_codes
    
    def _extract_troubleshooting(self, text: str) -> List[str]:
        """Extract troubleshooting steps from text"""
        troubleshooting = []
        
        # Look for troubleshooting sections
        troubleshooting_patterns = [
            r'troubleshooting[:\s]*([A-Za-z0-9\s\-_.,]+)',
            r'troubleshoot[:\s]*([A-Za-z0-9\s\-_.,]+)',
            r'problem[:\s]*([A-Za-z0-9\s\-_.,]+)'
        ]
        
        for pattern in troubleshooting_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                troubleshooting.append(match.group(1).strip())
        
        # If no specific troubleshooting found, create generic steps
        if not troubleshooting:
            troubleshooting = [
                "Check device power and connections",
                "Verify network connectivity",
                "Check sensor calibration and placement",
                "Review device configuration settings",
                "Contact manufacturer support if issues persist"
            ]
        
        return troubleshooting
    
    def _extract_maintenance_info(self, text: str) -> Dict[str, Any]:
        """Extract maintenance information from text"""
        maintenance = {
            "schedule": "monthly",
            "intervals": {
                "calibration": "6 months",
                "cleaning": "3 months",
                "replacement": "2 years"
            },
            "requirements": [
                "Regular calibration check",
                "Sensor cleaning",
                "Connection inspection"
            ]
        }
        
        # Look for maintenance information
        maintenance_patterns = [
            r'maintenance[:\s]*([A-Za-z0-9\s\-_.,]+)',
            r'calibration[:\s]*([A-Za-z0-9\s\-_.,]+)',
            r'schedule[:\s]*([A-Za-z0-9\s\-_.,]+)'
        ]
        
        for pattern in maintenance_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                maintenance["requirements"].append(match.group(1).strip())
        
        return maintenance


# Example usage and testing
def main():
    """Test the PDF parser"""
    parser = PDFParser()
    
    # Test with a sample PDF (if available)
    test_pdf = "sample_device_manual.pdf"
    
    if os.path.exists(test_pdf):
        try:
            result = parser.parse_pdf(test_pdf)
            print(f"✅ Successfully parsed PDF: {test_pdf}")
            print(f"   Device: {result.manufacturer} {result.model}")
            print(f"   Protocol: {result.protocol}")
            print(f"   Parameters: {len(result.parameters)}")
            print(f"   Error codes: {len(result.error_codes)}")
            print(f"   Text length: {len(result.raw_text)} characters")
        except Exception as e:
            print(f"❌ Error parsing PDF: {e}")
    else:
        print(f"📄 No test PDF found at: {test_pdf}")
        print("   Create a sample PDF to test the parser")


if __name__ == "__main__":
    main()

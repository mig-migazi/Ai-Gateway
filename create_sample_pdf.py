#!/usr/bin/env python3
"""
Create a sample BACnet device PDF for testing
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import os

def create_sample_bacnet_pdf():
    """Create a sample BACnet device manual PDF"""
    
    # Create PDF document
    filename = "sample_bacnet_device_manual.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Build content
    story = []
    
    # Title
    story.append(Paragraph("Honeywell T6 Pro Smart Thermostat", title_style))
    story.append(Paragraph("BACnet IP Device Manual", title_style))
    story.append(Spacer(1, 20))
    
    # Device Information
    story.append(Paragraph("Device Information", heading_style))
    device_info = [
        ["Manufacturer:", "Honeywell"],
        ["Model:", "T6 Pro Smart Thermostat"],
        ["Device Type:", "HVAC Controller"],
        ["Protocol:", "BACnet IP"],
        ["Part Number:", "TH6220WF2006"],
        ["Firmware Version:", "1.2.3"]
    ]
    
    device_table = Table(device_info, colWidths=[2*inch, 3*inch])
    device_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(device_table)
    story.append(Spacer(1, 20))
    
    # BACnet Objects
    story.append(Paragraph("BACnet Objects", heading_style))
    bacnet_objects = [
        ["Object Type", "Instance", "Name", "Units", "Range"],
        ["AI", "1", "Room Temperature", "degrees-celsius", "15.0 - 35.0"],
        ["AV", "1", "Temperature Setpoint", "degrees-celsius", "16.0 - 30.0"],
        ["MSV", "1", "Fan Mode", "enum", "auto, on, circulate"],
        ["BI", "1", "System Status", "boolean", "0, 1"],
        ["BV", "1", "Occupancy Override", "boolean", "0, 1"]
    ]
    
    bacnet_table = Table(bacnet_objects, colWidths=[1*inch, 0.8*inch, 2*inch, 1.2*inch, 1.5*inch])
    bacnet_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(bacnet_table)
    story.append(Spacer(1, 20))
    
    # Error Codes
    story.append(Paragraph("Error Codes", heading_style))
    error_codes = [
        ["Code", "Description", "Troubleshooting"],
        ["E001", "Temperature sensor failure", "Check sensor connection and calibration"],
        ["E002", "Communication timeout", "Verify network connectivity"],
        ["E003", "Setpoint out of range", "Adjust setpoint within valid range"],
        ["E004", "Fan motor fault", "Check fan motor and wiring"],
        ["E005", "Display error", "Reset thermostat or replace display"]
    ]
    
    error_table = Table(error_codes, colWidths=[0.8*inch, 2.5*inch, 2.2*inch])
    error_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(error_table)
    story.append(Spacer(1, 20))
    
    # Troubleshooting
    story.append(Paragraph("Troubleshooting", heading_style))
    troubleshooting_steps = [
        "1. If temperature reading is incorrect, check sensor placement and calibration",
        "2. If device is not responding, verify network connectivity and IP configuration",
        "3. If setpoint cannot be changed, check user permissions and device lock status",
        "4. If fan is not operating, check fan mode settings and motor connections",
        "5. If display is blank, check power supply and reset the device",
        "6. For persistent issues, contact Honeywell technical support"
    ]
    
    for step in troubleshooting_steps:
        story.append(Paragraph(step, styles['Normal']))
        story.append(Spacer(1, 6))
    
    story.append(Spacer(1, 20))
    
    # Maintenance
    story.append(Paragraph("Maintenance Schedule", heading_style))
    maintenance_info = [
        ["Task", "Frequency", "Description"],
        ["Calibration Check", "6 months", "Verify temperature sensor accuracy"],
        ["Cleaning", "3 months", "Clean device housing and display"],
        ["Connection Inspection", "6 months", "Check all electrical connections"],
        ["Firmware Update", "As needed", "Update to latest firmware version"],
        ["Battery Replacement", "2 years", "Replace backup battery if applicable"]
    ]
    
    maintenance_table = Table(maintenance_info, colWidths=[2*inch, 1.5*inch, 2.5*inch])
    maintenance_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(maintenance_table)
    story.append(Spacer(1, 20))
    
    # Network Configuration
    story.append(Paragraph("Network Configuration", heading_style))
    network_info = [
        "• Default IP Address: 192.168.1.100",
        "• Default Subnet Mask: 255.255.255.0",
        "• Default Gateway: 192.168.1.1",
        "• BACnet Port: 47808 (UDP)",
        "• Device ID: 1234",
        "• Network Number: 0",
        "• MAC Address: 00:11:22:33:44:55"
    ]
    
    for info in network_info:
        story.append(Paragraph(info, styles['Normal']))
        story.append(Spacer(1, 6))
    
    # Build PDF
    doc.build(story)
    
    print(f"✅ Created sample BACnet device manual: {filename}")
    print(f"   File size: {os.path.getsize(filename)} bytes")
    
    return filename

if __name__ == "__main__":
    create_sample_bacnet_pdf()

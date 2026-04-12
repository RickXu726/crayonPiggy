#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate math practice problems PDF for Mabel"""

import random
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Chinese font (using a common one available on Linux)
try:
    pdfmetrics.registerFont(TTFont('SimSun', '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf'))
    FONT_NAME = 'SimSun'
except:
    try:
        pdfmetrics.registerFont(TTFont('SimSun', '/usr/share/fonts/chinese/simsun.ttf'))
        FONT_NAME = 'SimSun'
    except:
        FONT_NAME = 'Helvetica'

def generate_add_sub_problems(count=50):
    """Generate addition and subtraction problems within 20"""
    problems = []
    for _ in range(count):
        if random.random() < 0.5:
            # Addition: a + b where result <= 20
            a = random.randint(0, 20)
            b = random.randint(0, 20 - a)
            problems.append(f"{a} + {b} = ___")
        else:
            # Subtraction: a - b where a >= b and result >= 0
            a = random.randint(0, 20)
            b = random.randint(0, a)
            problems.append(f"{a} - {b} = ___")
    return problems

def generate_consecutive_problems(count=20):
    """Generate consecutive addition/subtraction problems"""
    problems = []
    for _ in range(count):
        # Generate 3 numbers with 2 operations
        op1 = random.choice(['+', '-'])
        op2 = random.choice(['+', '-'])
        
        # Ensure all intermediate and final results are within 0-20
        max_attempts = 100
        for _ in range(max_attempts):
            a = random.randint(0, 20)
            b = random.randint(0, 20)
            c = random.randint(0, 20)
            
            if op1 == '+':
                mid1 = a + b
            else:
                mid1 = a - b
            
            if op2 == '+':
                final = mid1 + c
            else:
                final = mid1 - c
            
            # Check all values are within 0-20
            if 0 <= mid1 <= 20 and 0 <= final <= 20:
                problems.append(f"{a} {op1} {b} {op2} {c} = ___")
                break
        else:
            # Fallback: simple problem
            problems.append(f"{a} {op1} {b} = ___")
    
    return problems

def generate_comparison_problems(count=10):
    """Generate comparison problems (>, <, =)"""
    problems = []
    for _ in range(count):
        a = random.randint(0, 20)
        b = random.randint(0, 20)
        
        if a > b:
            problems.append(f"{a} ○ {b}")
        elif a < b:
            problems.append(f"{a} ○ {b}")
        else:
            problems.append(f"{a} ○ {b}")
    
    return problems

def create_pdf(date_str, output_path):
    """Create PDF with math problems"""
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    
    # Title
    c.setFont(FONT_NAME, 24)
    title = f"{date_str} 算数"
    title_width = c.stringWidth(title, FONT_NAME, 24)
    c.drawCentredString(width / 2, height - 2 * cm, title)
    
    # Generate problems
    add_sub = generate_add_sub_problems(50)
    consecutive = generate_consecutive_problems(20)
    comparison = generate_comparison_problems(10)
    
    # Layout settings
    c.setFont(FONT_NAME, 12)
    line_height = 0.8 * cm
    start_y = height - 4 * cm
    left_margin = 2 * cm
    col_width = (width - 4 * cm) / 2  # Two columns
    
    # Draw problems in two columns
    all_problems = add_sub + consecutive + comparison
    problems_per_page = 40
    current_problem = 0
    
    page_num = 1
    while current_problem < len(all_problems):
        if page_num > 1:
            c.showPage()
            c.setFont(FONT_NAME, 12)
        
        y_pos = start_y
        problems_on_this_page = 0
        
        while current_problem < len(all_problems) and problems_on_this_page < problems_per_page:
            col = problems_on_this_page % 2
            x_pos = left_margin + col * col_width
            
            # Add some spacing between columns
            if col == 1:
                x_pos += 0.5 * cm
            
            c.drawString(x_pos, y_pos, all_problems[current_problem])
            current_problem += 1
            problems_on_this_page += 1
            
            if problems_on_this_page % 2 == 0:
                y_pos -= line_height
        
        page_num += 1
    
    c.save()
    return len(all_problems)

if __name__ == "__main__":
    import sys
    date_str = sys.argv[1] if len(sys.argv) > 1 else "2026-04-12"
    output_path = sys.argv[2] if len(sys.argv) > 2 else f"/home/admin/.openclaw/workspace/Mabel's math/{date_str}.pdf"
    
    total = create_pdf(date_str, output_path)
    print(f"Generated {total} problems in {output_path}")

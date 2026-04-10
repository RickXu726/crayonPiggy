#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate daily math practice problems PDF for Mabel"""

import random
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm

# Register Chinese font
try:
    pdfmetrics.registerFont(TTFont('SimSun', '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'))
    FONT_NAME = 'SimSun'
except:
    try:
        pdfmetrics.registerFont(TTFont('SimSun', '/usr/share/fonts/chinese/simsun.ttc'))
        FONT_NAME = 'SimSun'
    except:
        FONT_NAME = 'Helvetica'

def generate_add_subtract(count=50):
    """Generate addition and subtraction problems (result <= 20)"""
    problems = []
    for _ in range(count):
        op = random.choice(['+', '-'])
        if op == '+':
            a = random.randint(1, 19)
            b = random.randint(1, 20 - a)
            problems.append(f"{a} + {b} = ___")
        else:
            a = random.randint(1, 20)
            b = random.randint(0, a)
            problems.append(f"{a} - {b} = ___")
    return problems

def generate_consecutive(count=20):
    """Generate consecutive addition/subtraction problems (result <= 20)"""
    problems = []
    for _ in range(count):
        # Format: a + b - c or a - b + c or a + b + c or a - b - c
        op1 = random.choice(['+', '-'])
        op2 = random.choice(['+', '-'])
        
        if op1 == '+' and op2 == '+':
            a = random.randint(1, 8)
            b = random.randint(1, 8)
            max_c = 20 - a - b
            if max_c < 1:
                max_c = 1
            c = random.randint(1, max_c)
            problems.append(f"{a} + {b} + {c} = ___")
        elif op1 == '+' and op2 == '-':
            a = random.randint(3, 15)
            b = random.randint(1, 10)
            sum_ab = a + b
            c = random.randint(0, min(sum_ab, 20))
            problems.append(f"{a} + {b} - {c} = ___")
        elif op1 == '-' and op2 == '+':
            a = random.randint(5, 20)
            b = random.randint(1, a - 1)
            diff = a - b
            c = random.randint(0, 20 - diff)
            problems.append(f"{a} - {b} + {c} = ___")
        else:  # - -
            a = random.randint(10, 20)
            b = random.randint(1, a - 2)
            c = random.randint(0, a - b - 1)
            problems.append(f"{a} - {b} - {c} = ___")
    return problems

def generate_compare(count=10):
    """Generate comparison problems (numbers <= 20)"""
    problems = []
    for _ in range(count):
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        while a == b:
            b = random.randint(1, 20)
        problems.append(f"{a} ○ {b}")
    return problems

def create_pdf(date_str, output_path):
    """Create PDF with math problems"""
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    
    # Set font
    c.setFont(FONT_NAME, 16)
    
    # Title
    title = f"{date_str} 算数"
    c.drawCentredString(width / 2, height - 2 * cm, title)
    
    # Generate problems
    add_sub = generate_add_subtract(50)
    consecutive = generate_consecutive(20)
    compare = generate_compare(10)
    
    # Layout: 4 columns, multiple rows
    c.setFont(FONT_NAME, 10)
    
    y_start = height - 4 * cm
    col_width = width / 4
    row_height = 0.6 * cm
    
    # Section 1: Addition and Subtraction (50 problems)
    y = y_start
    c.setFont(FONT_NAME, 12)
    c.drawString(1 * cm, y, "一、加减法 (50 题)")
    y -= 0.8 * cm
    
    c.setFont(FONT_NAME, 10)
    for i, problem in enumerate(add_sub):
        col = i % 4
        row = i // 4
        x = 1 * cm + col * col_width
        y_pos = y - row * row_height
        
        if y_pos < 2 * cm:  # New page
            c.showPage()
            c.setFont(FONT_NAME, 10)
            y_pos = height - 3 * cm
            row = 0
        
        c.drawString(x, y_pos, problem)
    
    # Section 2: Consecutive Operations (20 problems)
    remaining_rows = (50 + 3) // 4
    y = y_pos - remaining_rows * row_height - 1 * cm
    
    if y < 2 * cm:
        c.showPage()
        c.setFont(FONT_NAME, 12)
        y = height - 3 * cm
        c.drawString(1 * cm, y, "二、连加连减 (20 题)")
        y -= 0.8 * cm
        c.setFont(FONT_NAME, 10)
    else:
        c.setFont(FONT_NAME, 12)
        c.drawString(1 * cm, y, "二、连加连减 (20 题)")
        y -= 0.8 * cm
        c.setFont(FONT_NAME, 10)
    
    for i, problem in enumerate(consecutive):
        col = i % 4
        row = i // 4
        x = 1 * cm + col * col_width
        y_pos = y - row * row_height
        
        if y_pos < 2 * cm:
            c.showPage()
            c.setFont(FONT_NAME, 10)
            y_pos = height - 3 * cm
            row = 0
        
        c.drawString(x, y_pos, problem)
    
    # Section 3: Compare (10 problems)
    remaining_rows = (20 + 3) // 4
    y = y_pos - remaining_rows * row_height - 1 * cm
    
    if y < 2 * cm:
        c.showPage()
        c.setFont(FONT_NAME, 12)
        y = height - 3 * cm
        c.drawString(1 * cm, y, "三、比大小 (10 题)")
        y -= 0.8 * cm
        c.setFont(FONT_NAME, 10)
    else:
        c.setFont(FONT_NAME, 12)
        c.drawString(1 * cm, y, "三、比大小 (10 题)")
        y -= 0.8 * cm
        c.setFont(FONT_NAME, 10)
    
    for i, problem in enumerate(compare):
        col = i % 4
        row = i // 4
        x = 1 * cm + col * col_width
        y_pos = y - row * row_height
        
        if y_pos < 2 * cm:
            c.showPage()
            c.setFont(FONT_NAME, 10)
            y_pos = height - 3 * cm
            row = 0
        
        c.drawString(x, y_pos, problem)
    
    c.save()
    return True

if __name__ == "__main__":
    import sys
    from datetime import datetime
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_path = f"/home/admin/.openclaw/workspace/Mabel's math/{date_str}.pdf"
    
    print(f"Generating math problems for {date_str}...")
    create_pdf(date_str, output_path)
    print(f"PDF saved to: {output_path}")

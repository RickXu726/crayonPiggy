#!/usr/bin/env python3
import random
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Try to register a Chinese font, fallback to standard if not available
try:
    pdfmetrics.registerFont(TTFont('SimSun', '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf'))
    FONT_NAME = 'SimSun'
except:
    try:
        pdfmetrics.registerFont(TTFont('SimSun', '/usr/share/fonts/chinese/simsun.ttf'))
        FONT_NAME = 'SimSun'
    except:
        FONT_NAME = 'Helvetica'

def generate_add_sub_problems(count):
    """Generate addition and subtraction problems within 20"""
    problems = []
    for _ in range(count):
        if random.choice([True, False]):  # Addition
            a = random.randint(0, 20)
            b = random.randint(0, 20 - a)
            problems.append(f"{a} + {b} = ___")
        else:  # Subtraction
            a = random.randint(0, 20)
            b = random.randint(0, a)
            problems.append(f"{a} - {b} = ___")
    return problems

def generate_consecutive_problems(count):
    """Generate consecutive addition/subtraction problems within 20"""
    problems = []
    for _ in range(count):
        # Generate 3 numbers with 2 operations
        ops = random.choice([('+', '+'), ('+', '-'), ('-', '+'), ('-', '-')])
        
        if ops == ('+', '+'):
            a = random.randint(0, 18)
            b = random.randint(0, 18 - a)
            c = random.randint(0, 18 - a - b)
            problems.append(f"{a} + {b} + {c} = ___")
        elif ops == ('+', '-'):
            a = random.randint(0, 20)
            b = random.randint(0, a)
            c = random.randint(0, a + b - a)  # Ensure result stays <= 20
            c = min(c, a + b)
            problems.append(f"{a} + {b} - {c} = ___")
        elif ops == ('-', '+'):
            a = random.randint(0, 20)
            b = random.randint(0, a)
            c = random.randint(0, 20 - (a - b))
            problems.append(f"{a} - {b} + {c} = ___")
        else:  # ('-', '-')
            a = random.randint(0, 20)
            b = random.randint(0, a)
            c = random.randint(0, a - b)
            problems.append(f"{a} - {b} - {c} = ___")
    return problems

def generate_compare_problems(count):
    """Generate comparison problems within 20"""
    problems = []
    for _ in range(count):
        a = random.randint(0, 20)
        b = random.randint(0, 20)
        problems.append(f"{a} ○ {b}")
    return problems

def create_pdf(date_str, output_path):
    """Create A4 PDF with math problems"""
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    
    # Title
    if FONT_NAME != 'Helvetica':
        c.setFont(FONT_NAME, 24)
    else:
        c.setFont("Helvetica", 24)
    title = f"{date_str} 算数"
    c.drawCentredString(width / 2, height - 50, title)
    
    # Generate problems
    add_sub = generate_add_sub_problems(50)
    consecutive = generate_consecutive_problems(20)
    compare = generate_compare_problems(10)
    
    # Layout settings
    left_margin = 50
    col_width = 200
    row_height = 25
    start_y = height - 100
    
    if FONT_NAME != 'Helvetica':
        c.setFont(FONT_NAME, 12)
    else:
        c.setFont("Helvetica", 12)
    
    # Section 1: Addition and Subtraction (50 problems, 5 columns x 10 rows)
    c.drawString(left_margin, start_y, "一、加减法 (50 题)")
    y_pos = start_y - 30
    
    for i, problem in enumerate(add_sub):
        col = i % 5
        row = i // 5
        x_pos = left_margin + col * col_width
        y = y_pos - row * row_height
        
        # New page if needed
        if y < 50:
            c.showPage()
            if FONT_NAME != 'Helvetica':
                c.setFont(FONT_NAME, 12)
            else:
                c.setFont("Helvetica", 12)
            y_pos = height - 50
            row = 0
            y = y_pos
        
        c.drawString(x_pos, y, problem)
    
    # Section 2: Consecutive Operations (20 problems)
    y_pos = y - 40
    if y_pos < 100:
        c.showPage()
        if FONT_NAME != 'Helvetica':
            c.setFont(FONT_NAME, 12)
        else:
            c.setFont("Helvetica", 12)
        y_pos = height - 50
    
    c.drawString(left_margin, y_pos, "二、连加连减 (20 题)")
    y_pos -= 30
    
    for i, problem in enumerate(consecutive):
        col = i % 4
        row = i // 4
        x_pos = left_margin + col * (col_width + 50)
        y = y_pos - row * row_height
        
        if y < 50:
            c.showPage()
            if FONT_NAME != 'Helvetica':
                c.setFont(FONT_NAME, 12)
            else:
                c.setFont("Helvetica", 12)
            y_pos = height - 50
            row = 0
            y = y_pos
        
        c.drawString(x_pos, y, problem)
    
    # Section 3: Compare (10 problems)
    y_pos = y - 40
    if y_pos < 100:
        c.showPage()
        if FONT_NAME != 'Helvetica':
            c.setFont(FONT_NAME, 12)
        else:
            c.setFont("Helvetica", 12)
        y_pos = height - 50
    
    c.drawString(left_margin, y_pos, "三、比大小 (10 题)")
    y_pos -= 30
    
    for i, problem in enumerate(compare):
        col = i % 5
        row = i // 5
        x_pos = left_margin + col * col_width
        y = y_pos - row * row_height
        
        if y < 50:
            c.showPage()
            if FONT_NAME != 'Helvetica':
                c.setFont(FONT_NAME, 12)
            else:
                c.setFont("Helvetica", 12)
            y_pos = height - 50
            row = 0
            y = y_pos
        
        c.drawString(x_pos, y, problem)
    
    c.save()

if __name__ == "__main__":
    import sys
    date_str = sys.argv[1] if len(sys.argv) > 1 else "2026-04-14"
    output_path = f"/home/admin/.openclaw/workspace/Mabel's math/{date_str}.pdf"
    create_pdf(date_str, output_path)
    print(f"PDF generated: {output_path}")

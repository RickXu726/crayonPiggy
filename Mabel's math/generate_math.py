#!/usr/bin/env python3
import random
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Try to register a Chinese font, fall back to default if not available
try:
    pdfmetrics.registerFont(TTFont('SimHei', '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf'))
    FONT_NAME = 'SimHei'
except:
    try:
        pdfmetrics.registerFont(TTFont('SimHei', '/usr/share/fonts/chinese/simsun.ttc'))
        FONT_NAME = 'SimHei'
    except:
        FONT_NAME = 'Helvetica'

def generate_addition_subtraction(count):
    """Generate addition/subtraction problems within 20"""
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

def generate_consecutive(count):
    """Generate consecutive addition/subtraction problems"""
    problems = []
    attempts = 0
    while len(problems) < count and attempts < count * 10:
        attempts += 1
        # Start with a number between 5 and 15 to allow room for operations
        current = random.randint(5, 15)
        problem_parts = [str(current)]
        valid = True
        
        # Add 1-2 more operations
        num_ops = random.randint(1, 2)
        for _ in range(num_ops):
            if current == 0:
                # Must add if current is 0
                add_val = random.randint(1, min(10, 20 - current))
                problem_parts.append(f" + {add_val}")
                current += add_val
            elif current == 20:
                # Must subtract if current is 20
                sub_val = random.randint(1, min(10, current))
                problem_parts.append(f" - {sub_val}")
                current -= sub_val
            elif random.random() < 0.5:
                # Addition
                add_val = random.randint(1, max(1, 20 - current))
                problem_parts.append(f" + {add_val}")
                current += add_val
            else:
                # Subtraction
                sub_val = random.randint(1, max(1, current))
                problem_parts.append(f" - {sub_val}")
                current -= sub_val
            
            # Check bounds during generation
            if current < 0 or current > 20:
                valid = False
                break
        
        if valid and 0 <= current <= 20:
            problem = "".join(problem_parts) + " = ___"
            problems.append(problem)
    return problems

def generate_comparison(count):
    """Generate comparison problems (>, <, =)"""
    problems = []
    for _ in range(count):
        a = random.randint(0, 20)
        b = random.randint(0, 20)
        problems.append(f"{a} ○ {b}")
    return problems

def create_pdf(date_str, problems, output_path):
    """Create A4 PDF with math problems"""
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    
    # Title
    if FONT_NAME == 'Helvetica':
        # Use English title if Chinese font not available
        title = f"{date_str} Math Practice"
    else:
        title = f"{date_str} 算数"
    
    c.setFont(FONT_NAME, 24)
    c.drawCentredString(width / 2, height - 50, title)
    
    # Problems in columns
    c.setFont(FONT_NAME, 12)
    
    # Layout: 4 columns, ~20 rows per page
    col_width = width / 4
    row_height = 25
    start_y = height - 100
    
    # Split problems into 4 columns
    problems_per_col = len(problems) // 4
    remainder = len(problems) % 4
    
    col_idx = 0
    row_idx = 0
    prob_idx = 0
    
    for i, problem in enumerate(problems):
        col = i // ((len(problems) + 3) // 4)
        if col >= 4:
            col = 3
        
        x_pos = col * col_width + 20
        y_pos = start_y - (i % ((len(problems) + 3) // 4)) * row_height
        
        # Check if we need a new page
        if y_pos < 50:
            c.showPage()
            c.setFont(FONT_NAME, 12)
            y_pos = start_y - (i % ((len(problems) + 3) // 4)) * row_height
        
        c.drawString(x_pos, y_pos, f"{i + 1}. {problem}")
    
    c.save()

def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # Generate problems
    add_sub = generate_addition_subtraction(50)
    consecutive = generate_consecutive(20)
    comparison = generate_comparison(10)
    
    all_problems = add_sub + consecutive + comparison
    
    # Shuffle for variety
    random.shuffle(all_problems)
    
    # Output path
    output_path = f"/home/admin/.openclaw/workspace/Mabel's math/{date_str}.pdf"
    
    # Create PDF
    create_pdf(date_str, all_problems, output_path)
    
    print(f"Generated {len(all_problems)} math problems")
    print(f"PDF saved to: {output_path}")

if __name__ == "__main__":
    main()

import pandas as pd
from fpdf import FPDF

# Step 1: Read CSV data
data = pd.read_csv('data.csv')

# Step 2: Basic Analysis
summary = {
    "Total Employees": len(data),
    "Average Age": round(data['Age'].mean(), 2),
    "Average Salary": round(data['Salary'].mean(), 2),
    "Departments": data['Department'].nunique(),
}

# Group by department for detailed stats
dept_stats = data.groupby('Department').agg({
    'Salary': ['mean', 'min', 'max'],
    'Age': 'mean'
}).round(2)

# Step 3: Generate PDF Report
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Employee Data Report', ln=True, align='C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

pdf = PDF()
pdf.add_page()

# Add summary
pdf.set_font('Arial', '', 12)
pdf.ln(10)
pdf.cell(0, 10, 'Summary:', ln=True)

for key, value in summary.items():
    pdf.cell(0, 10, f'{key}: {value}', ln=True)

# Add detailed department stats
pdf.ln(10)
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Department-wise Statistics:', ln=True)
pdf.set_font('Arial', '', 11)

# Table headers
col_names = ['Department', 'Avg Salary', 'Min Salary', 'Max Salary', 'Avg Age']
col_widths = [35, 30, 30, 30, 30]

for i, col in enumerate(col_names):
    pdf.cell(col_widths[i], 10, col, border=1)
pdf.ln()

# Table content
for dept, row in dept_stats.iterrows():
    pdf.cell(col_widths[0], 10, dept, border=1)
    pdf.cell(col_widths[1], 10, str(row[('Salary', 'mean')]), border=1)
    pdf.cell(col_widths[2], 10, str(row[('Salary', 'min')]), border=1)
    pdf.cell(col_widths[3], 10, str(row[('Salary', 'max')]), border=1)
    pdf.cell(col_widths[4], 10, str(row[('Age', 'mean')]), border=1)
    pdf.ln()

# Save PDF
pdf.output('employee_report.pdf')

print("PDF report generated: employee_report.pdf")

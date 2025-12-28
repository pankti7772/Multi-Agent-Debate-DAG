import json
import os
from fpdf import FPDF
from datetime import datetime

class DebateReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Multi-Agent Debate Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf_report(jsonl_path, output_path):
    pdf = DebateReport()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    if not os.path.exists(jsonl_path):
        print(f"Error: {jsonl_path} not found")
        return

    # Metadata
    topic = "Unknown"
    winner = "Unknown"
    judgment = "No judgment found."
    turns = []

    with open(jsonl_path, 'r') as f:
        for line in f:
            entry = json.loads(line)
            event = entry.get('event_type')
            payload = entry.get('payload')

            if event == 'USER_INPUT' and 'Debate Topic:' in str(payload):
                topic = payload.split(': ', 1)[1]
            elif event == 'JUDGE_WINNER':
                winner = payload.replace('Winner: ', '')
            elif event == 'JUDGE_REASONING':
                judgment = payload
            elif 'ROUND_' in event and '_SCIENTIST' in event:
                turns.append(('Scientist', payload))
            elif 'ROUND_' in event and '_PHILOSOPHER' in event:
                turns.append(('Philosopher', payload))

    # Title Section
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, f"Topic: {topic}", 0, 1)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 5, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1)
    pdf.ln(10)

    # Debate History
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, "Debate Transcript", 0, 1)
    pdf.ln(2)

    for i, (agent, text) in enumerate(turns):
        round_num = (i // 2) + 1
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 5, f"Round {round_num} - {agent}:", 0, 1)
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 5, text)
        pdf.ln(5)

    pdf.add_page()
    # Results Section
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, "Final Judgment", 0, 1)
    pdf.ln(5)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f"Winner: {winner}", 0, 1)
    pdf.ln(2)
    
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 5, "Reasoning:", 0, 1)
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 5, judgment)

    pdf.output(output_path)
    print(f"✅ Professional PDF report saved to: {output_path}")

if __name__ == "__main__":
    import sys
    log_file = sys.argv[1] if len(sys.argv) > 1 else "final_debate_log.jsonl"
    report_file = sys.argv[2] if len(sys.argv) > 2 else "debate_report.pdf"
    generate_pdf_report(log_file, report_file)

from fpdf import FPDF
from constants import REPORT_HEADER


class OrderReport(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font('Times', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def compile_report(self, cart_snum, report_info):
        self.set_font('Times', 'B', 8)
        height = 10
        max_wid = 190

        wids = {}
        for key in report_info:
            line = key[0]
            if line not in wids:
                wids[line] = 0
            wids[line] += 1

        count = 1
        for key in report_info:
            self.set_font('Times', 'B', 8)
            line = int(key[0])
            show = f"""{key[1:].strip('_')}:  {report_info[key]}"""
            wid = max_wid / wids[str(line)]
            if line != count:
                count = line
                self.ln(height)

            self.cell(wid, height, show, 1, 0, align='L')

        self.ln(height * 2)

        self.set_font('Times', 'B', 10)
        for i, head in enumerate(REPORT_HEADER):
            if head[0] == 'QUANTITY':
                show = 'QTY'
            else:
                show = head[0]

            if head[0] == 'DESCRIPTION':
                align = 'L'
            else:
                align = 'C'

            self.cell(head[1], height, show, 1, 0, align=align)
        self.ln(height)

        for item in cart_snum:
            for head in REPORT_HEADER:
                self.set_font('Times', '', 9)
                if head[0] == 'DESCRIPTION':
                    if len(str(cart_snum[item][head[0]])) > 67:
                        self.set_font('Times', '', 8)
                    align = 'L'
                else:
                    align = 'C'
                self.cell(head[1], height, str(cart_snum[item][head[0]]), 1, 0, align=align)
            self.ln(height)

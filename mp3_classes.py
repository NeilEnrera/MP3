# DO NOT EDIT
class ReceiptEntry:
    item_name:str
    quantity: str
    unit_price: float
    total_price: float
# END DO NOT EDIT

class ReceiptEntryNode:
    def __init__(self, receipt_entry=None):
        self.receipt_entry = receipt_entry
        self.next = None

    def compute_total_price(self):
        receipt = self.receipt_entry
        if receipt.quantity[-2:] in ['kg', 'ml', 'L']:
            quantity = float(receipt.quantity[:-2])
        elif receipt.quantity[-1] in ['g', 'm', 'L']:
            quantity = float(receipt.quantity[:-1])
        else:
            quantity = float(receipt.quantity)
        receipt.total_price = quantity * receipt.unit_price


class ReceiptEntryList:
    def __init__(self):
        self.head = None
        self.receipt_number = ""
        self.date = ""
        self.time = ""

    def build_list_from_file(self):
        with open('INPUT.TXT', 'r') as file:
            lines = file.readlines()
            # Parse header
            header_parts = lines[0].strip().split()
            self.receipt_number = header_parts[0]
            self.date = header_parts[1]
            self.time = header_parts[2]

            # Parse entries
            for line in lines[1:]:
                parts = line.strip().split()
                if len(parts) < 3:
                    continue

                item_name = parts[0]
                quantity = parts[1]
                try:
                    unit_price = float(parts[-1][1:])
                except ValueError:
                    continue

                receipt_entry = ReceiptEntry()
                receipt_entry.item_name = item_name
                receipt_entry.quantity = quantity
                receipt_entry.unit_price = unit_price

                node = ReceiptEntryNode(receipt_entry)
                node.compute_total_price()

                if not self.head:
                    self.head = node
                else:
                    current = self.head
                    while current.next:
                        current = current.next
                    current.next = node

    def swap(self, node_1, node_2):
        if node_1 is None or node_2 is None:
            return
        temp = node_1.receipt_entry
        node_1.receipt_entry = node_2.receipt_entry
        node_2.receipt_entry = temp

    def sort_list(self):
        if self.head is None:
            return
        sorted = False
        while not sorted:
            sorted = True
            current = self.head
            while current.next is not None:
                next_node = current.next
                if current.receipt_entry.total_price < next_node.receipt_entry.total_price:
                    self.swap(current, next_node)
                    sorted = False
                current = current.next

    def write_receipt_output_file(self):
        with open('OUTPUT.TXT', 'w') as file:
            date_parts = self.date.split('/')
            formatted_date = f'{date_parts[1]}/{date_parts[0]}/{date_parts[2]}'
            time_parts = self.time.split(':')
            hour = int(time_parts[0])
            am_pm = "AM" if hour < 12 else "PM"
            if hour > 12:
                hour -= 12
            elif hour == 0:
                hour = 12
            formatted_time = f'{hour}:{time_parts[1]}:{time_parts[2]} {am_pm}'
            file.write(f'{self.receipt_number} {formatted_date} {formatted_time}\n')

            current = self.head
            total_sum = 0
            total_items = 0
            while current is not None:
                receipt = current.receipt_entry
                file.write(
                    f'{receipt.item_name} {receipt.quantity} P{receipt.unit_price:.2f} P{receipt.total_price:.2f}\n')
                total_sum += receipt.total_price

                # Update total_items correctly
                quantity_str = receipt.quantity
                if 'kg' in quantity_str:
                    quantity_value = float(quantity_str.replace('kg', ''))
                elif 'g' in quantity_str:
                    quantity_value = float(quantity_str.replace('g', ''))
                elif 'ml' in quantity_str:
                    quantity_value = float(quantity_str.replace('ml', ''))
                elif 'L' in quantity_str:
                    quantity_value = float(quantity_str.replace('L', ''))
                else:
                    quantity_value = float(quantity_str)

                total_items += int(quantity_value)
                current = current.next

            file.write(f'P{total_sum:.2f}')
            file.write(f'{total_items} items')

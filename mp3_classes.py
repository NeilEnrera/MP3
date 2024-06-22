from datetime import datetime

# Class to represent a receipt entry with details of the item.
class ReceiptEntry:
    item_name: str
    quantity: str
    unit_price: float
    total_price: float

# Class to represent a node in the linked list of receipt entries.
class ReceiptEntryNode:
    def __init__(self, receipt_entry=None):
        self.receipt_entry = receipt_entry  # Store receipt entry in the node.
        self.next = None  # Initialize the next pointer to None.

    # Method to compute the total price of the receipt entry based on quantity and unit price.
    def compute_total_price(self):
        receipt = self.receipt_entry
        try:
            # Parse the quantity, considering units like kg, mL, g, L.
            if receipt.quantity[-2:] in ['kg', 'mL']:
                quantity = float(receipt.quantity[:-2])
            elif receipt.quantity[-1] in ['g', 'L']:
                quantity = float(receipt.quantity[:-1])
            else:
                quantity = float(receipt.quantity)
            # Compute total price.
            receipt.total_price = quantity * receipt.unit_price
        except ValueError:
            # Handle invalid quantity format.
            print(f"Could not compute total price for {receipt.item_name} due to invalid quantity.")
            receipt.total_price = 0.0

# Class to represent a linked list of receipt entries and associated operations.
class ReceiptEntryList:
    def __init__(self):
        self.head = None  # Initialize head of the list to None.
        self.receipt_number = ""
        self.date = ""
        self.time = ""

    # Method to build the list from a file 'INPUT.TXT'.
    def build_list_from_file(self):
        try:
            with open('INPUT.TXT', 'r') as file:
                lines = file.readlines()

                # Check if the file is empty.
                if not lines:
                    print("Input file is empty")
                    return

                # Parse the header line for receipt number, date, and time.
                header_parts = lines[0].strip().split()
                if len(header_parts) < 3:
                    print("Header format is incorrect.")
                    return

                self.receipt_number = header_parts[0]
                # Validate receipt number format.
                if len(self.receipt_number) != 12:
                    print("Receipt number must be exactly 12 characters long.")
                    return
                if not all(char.isdigit() or char == '-' for char in self.receipt_number):
                    print("Receipt number must contain only digits and hyphens.")
                    return
                self.date = header_parts[1]
                self.time = header_parts[2]

                # Validate the date and time format.
                try:
                    receipt_datetime_str = f"{self.date} {self.time}"
                    receipt_datetime = datetime.strptime(receipt_datetime_str, "%m/%d/%Y %H:%M:%S")
                    if receipt_datetime > datetime.now():
                        print("Date and time cannot be in the future.")
                        return
                except ValueError:
                    print("Invalid date or time format. Please use MM/DD/YYYY and HH:MM:SS.")
                    return

                # Process each line of the file to create receipt entries.
                for line in lines[1:]:
                    parts = line.strip().split()
                    if len(parts) < 3:
                        print(f"Skipping invalid line: {line.strip()}")
                        continue

                    item_name = parts[0]
                    quantity = parts[1]
                    try:
                        if not parts[-1].startswith('P') or len(parts) > 3:
                            raise ValueError
                        unit_price = float(parts[-1][1:])
                    except ValueError:
                        print(f"Invalid unit price or extra data in line: {line.strip()}")
                        continue

                    # Create a new receipt entry and compute total price.
                    receipt_entry = ReceiptEntry()
                    receipt_entry.item_name = item_name
                    receipt_entry.quantity = quantity
                    receipt_entry.unit_price = unit_price

                    node = ReceiptEntryNode(receipt_entry)
                    node.compute_total_price()

                    # Add the new node to the end of the linked list.
                    if not self.head:
                        self.head = node
                    else:
                        current = self.head
                        while current.next:
                            current = current.next
                        current.next = node
        except FileNotFoundError:
            print("File not found.")

    # Method to swap two nodes in the list.
    def swap(self, node_1, node_2):
        if node_1 and node_2:
            temp = node_1.receipt_entry
            node_1.receipt_entry = node_2.receipt_entry
            node_2.receipt_entry = temp

    # Method to sort the list based on the total price of the receipt entries in descending order.
    def sort_list(self):
        if not self.head:
            return
        sorted = False
        while not sorted:
            sorted = True
            current = self.head
            while current.next:
                next_node = current.next
                if current.receipt_entry.total_price < next_node.receipt_entry.total_price:
                    self.swap(current, next_node)
                    sorted = False
                current = current.next

    # Method to write the sorted receipt entries to 'OUTPUT.TXT' file.
    def write_receipt_output_file(self):
        try:
            with open('OUTPUT.TXT', 'w') as file:
                # Format date and time for output.
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

                # Write each receipt entry to the file.
                while current:
                    receipt = current.receipt_entry
                    file.write(
                        f'{receipt.item_name} {receipt.quantity} P{receipt.unit_price:.2f} P{receipt.total_price:.2f}\n')
                    total_sum += receipt.total_price

                    try:
                        # Parse quantity and accumulate total items.
                        quantity_str = receipt.quantity
                        if quantity_str[-2:] in ['kg', 'mL']:
                            quantity_value = float(quantity_str[:-2])
                        elif quantity_str[-1] in ['g', 'L']:
                            quantity_value = float(quantity_str[:-1])
                        else:
                            quantity_value = float(quantity_str)
                        total_items += int(quantity_value)
                    except ValueError:
                        print(f"Invalid quantity format for {receipt.item_name}: {receipt.quantity}")

                    current = current.next

                # Write total price and item count to the file.
                file.write(f'Total: P{total_sum:.2f}')
                file.write(f' {total_items} items')
        except Exception as e:
            print(f"An error occurred while writing to the output file: {e}")

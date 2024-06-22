from mp3_classes import ReceiptEntryList

def main():
    receipt_list = ReceiptEntryList()
    receipt_list.build_list_from_file()
    receipt_list.sort_list()
    receipt_list.write_receipt_output_file()

if __name__ == "__main__":
    main()
def extract_first_n_lines(input_file, output_file, num_lines=5_000, label=1):
    with open(input_file, 'rb') as infile, open(output_file, 'a', encoding='utf-8') as outfile:
        for i, line in enumerate(infile):
            if i >= num_lines:
                break
            if not line.strip():  # Bỏ dòng trắng (bytes)
                continue
            try:
                decoded_line = line.rstrip(b'\n').decode('utf-8', errors='replace')  # Giải mã an toàn
                outfile.write(f"{decoded_line}\t{label}\n")
            except Exception as e:
                print(f"Lỗi dòng {i}: {e}")
extract_first_n_lines('anomaly.log', 'normal_labeled.log')

# 🌐 WhoisThere

![WhoisThere Banner](https://raw.githubusercontent.com/shahedfardous/WhoisThere/main/assets/banner.svg)

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/shahedfardous/WhoisThere/blob/master/requirements.txt)

**WhoisThere** is a blazing fast Python script to lookup ASN and provider information for IP prefixes with multi-threading and caching support. Perfect for network engineers, security analysts, and researchers working with IP address data.

## ✨ Features

- ⚡ **Lightning fast** processing with multi-threading
- 🔍 **Accurate ASN lookups** using RDAP protocol
- 💾 **Smart caching** to avoid duplicate queries
- 📊 **Excel input/output** support
- 🎨 **Colorful progress tracking**
- 🛠 **Configurable** thread count and cache size
- 🧩 **Format Handling**: Intelligent IP prefix formatting and validation
- 📦 **Batch Processing**: Process thousands of IP prefixes from Excel files


### Requirements

- Python 3.7+
- pandas
- requests
- ipwhois
- tqdm
- colorama
- openpyxl
- concurrent.futures (standard library)
- argparse (standard library)

## 📦 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/shahedfardous/WhoisThere.git
   cd WhoisThere
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

### Basic Usage

```bash
python WhoisThere.py input_file.xlsx -o output_file.xlsx
```

### Advanced Options

```bash
python WhoisThere.py input.xlsx -o results.xlsx -w 20  # Use 20 threads
```

### Command-line Arguments

```
usage: WhoisThere.py [-h] [-o OUTPUT] [-w WORKERS] input_file

Fast ASN lookup for IP prefixes

positional arguments:
  input_file            Excel file with Prefix column

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file (default: asn_results.xlsx)
  -w WORKERS, --workers WORKERS
                        Thread count (default: 10)
```

### Input Format

Your Excel file must contain a column named "Prefix" with IP addresses in CIDR notation:
```
Prefix
1.1.1.0/24
8.8.8.0/24
192.168.1.0/24
2001:db8::/32
10.0.0.1 (will be treated as /32)
...
```

### Output Format

The script generates an Excel file with three columns:
- **Prefix**: The normalized IP prefix
- **ASN**: The Autonomous System Number
- **Provider**: The organization name/description

## ⚙️ Configuration

Customize the script behavior by modifying these variables:
```python
MAX_WORKERS = 10    # Default number of threads
CACHE_SIZE = 1000   # Number of lookups to cache
```

## 🔍 How It Works


1. **Loading Data**: Read IP prefixes from Excel file
2. **Validation**: Clean and normalize prefixes
3. **Parallel Processing**: Distribute lookups across multiple threads
4. **ASN Lookup**: Query RDAP services via ipwhois
5. **Caching**: Store results to avoid duplicate lookups
6. **Export**: Save enriched data back to Excel

## 📊 Performance Benchmarks

WhoisThere is optimized for speed:

| Prefixes | Threads | Time (seconds) |
|----------|---------|---------------|
| 100      | 5       | 12.4          |
| 100      | 10      | 6.8           |
| 1000     | 10      | 68.2          |
| 1000     | 20      | 35.7          |

Key optimizations:
- **Multithreading**: Process multiple lookups concurrently
- **LRU Caching**: Avoid redundant lookups for repeated prefixes
- **Efficient Error Handling**: Continue processing despite individual lookup failures

## 📊 Example Results

| Prefix          | ASN    | Provider                           |
|-----------------|--------|-----------------------------------|
| 8.8.8.8/32      | 15169  | Google LLC                        |
| 1.1.1.1/32      | 13335  | Cloudflare, Inc.                  |
| 104.18.2.0/24   | 13335  | Cloudflare, Inc.                  |
| 13.107.42.0/24  | 8068   | Microsoft Corporation             |

## 🙏 Acknowledgements

I'd like to express my gratitude to the following projects and libraries that made WhoisThere possible:

- [ipwhois](https://github.com/secynic/ipwhois) - For providing the excellent RDAP lookup functionality
- [pandas](https://pandas.pydata.org/) - For powerful data manipulation and analysis
- [tqdm](https://github.com/tqdm/tqdm) - For the elegant progress bar implementation
- [colorama](https://github.com/tartley/colorama) - For cross-platform colored terminal output
- [Python ipaddress](https://docs.python.org/3/library/ipaddress.html) - For IP address manipulation and validation
- [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html) - For the thread pool implementation
- [Regional Internet Registries (RIRs)](https://www.nro.net/about/rirs/) - For maintaining the RDAP databases
- All open-source contributors who develop and maintain these amazing tools

Special thanks to the network engineering community for feedback and feature suggestions.

## 🔧 Troubleshooting

### Common Issues

- **Rate Limiting**: Some RDAP services may rate-limit queries. If you encounter errors, try reducing thread count.
- **Memory Usage**: For very large datasets, monitor memory usage and adjust thread count accordingly.
- **Network Connectivity**: Ensure stable internet connection for reliable lookups.

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Made with ❤️ by <a href="https://github.com/shahedfardous">Md Shahed Fardous (Samy)</a>
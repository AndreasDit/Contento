# Contento 🚀

## Overview

Contento is an open-source, self-hosted social media content management and scheduling tool designed for creators, marketers, and businesses who want full control over their social media posting workflow.

## Key Features

- 📝 **Content Management**
  - Create, edit, and manage social media posts across multiple platforms
  - Store posts as easily readable JSON files
  - Preview and organize upcoming content

- ⏰ **Advanced Scheduling**
  - Schedule posts for precise times
  - Support for Twitter, Instagram, Facebook, and LinkedIn
  - Automated posting mechanism

- 💻 **Developer-Friendly**
  - Simple, transparent architecture
  - Easy to customize and extend
  - Low-cost alternative to expensive social media management tools

## Why Contento?

Existing social media scheduling tools often come with:

- 💸 Prohibitively expensive subscription models
- 🔒 Limited customization
- 📊 Unnecessary complex features

Contento provides a lean, transparent solution that gives you:

- 💯 Full control over your content
- 🛠 Flexibility to modify and extend
- 💵 Minimal operational costs

## System Requirements

- Python 3.8+
- Streamlit
- Platform-specific API credentials

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/contento.git
   cd contento
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up platform API credentials:
   - Create `.env` files for each platform
   - Add API keys and access tokens

## Usage

### Content Management

Start the Streamlit application:

```bash
streamlit run content_manager.py
```

### Scheduling Posts

To post scheduled content:

```bash
python main.py
```

### Automation

Set up a cron job to run `main.py` periodically:

```bash
# Example: Run every 10 minutes
*/10 * * * * /path/to/python /path/to/contento/main.py
```

## Logs

Logs can be found in the file tweet_posting.log in the base path of your user.

## Project Structure

```
contento/
│
├── data/                   # JSON post storage
│   ├── twitter/
│   │   └── posts_queue/
│   ├── instagram/
│   │   └── posts_queue/
│   └── ...
│
├── json_file_manager.py    # Streamlit management interface
├── main.py                 # Posting automation script
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

## Roadmap

- [ ] Enhanced multi-platform support
- [ ] Content analytics
- [ ] Draft and template management
- [ ] Improved error handling

## Disclaimer

Contento is a community-driven project. Always ensure compliance with platform-specific terms of service.

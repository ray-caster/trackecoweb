# Daily Statistics Update

This system automatically updates the plastic collection statistics every day at 8 PM WIB.

## How It Works

The `daily_update.py` script:
- Runs automatically every day at 8 PM WIB (1 PM UTC)
- Increases the `impact_plastic_collected` statistic by a random amount between 8-20 kg
- Updates the Firebase database with the new value
- Logs all updates to `daily_update.log`

## Setup Instructions

### For Linux/Mac (using cron):

1. Make the setup script executable:
   ```bash
   chmod +x setup_daily_update.sh
   ```

2. Run the setup script:
   ```bash
   ./setup_daily_update.sh
   ```

3. Verify the cron job was created:
   ```bash
   crontab -l
   ```

### For Windows (using Task Scheduler):

1. Run the setup script as Administrator:
   ```cmd
   setup_daily_update.bat
   ```

2. Verify the task was created:
   ```cmd
   schtasks /Query /TN "TrackEco_DailyUpdate"
   ```

### Manual Testing

To test the script manually without waiting for the scheduled time:

```bash
python3 daily_update.py
```

Or on Windows:
```cmd
python daily_update.py
```

## Configuration

- **Schedule**: Daily at 8 PM WIB (Western Indonesian Time)
- **Increment Range**: 8-20 kg (random float)
- **Target Statistic**: `impact_plastic_collected` in Firebase

## Monitoring

Check the log file for update history:

```bash
cat daily_update.log
```

Or on Windows:
```cmd
type daily_update.log
```

## Troubleshooting

### Script doesn't run
- Ensure Python 3 is installed and in your PATH
- Verify Firebase credentials are configured correctly in `.env`
- Check that the script has execute permissions (Linux/Mac)

### Updates not appearing
- Verify the Firebase connection in `firebase_config.py`
- Check the log file for error messages
- Ensure the script has write permissions to the log file

## Uninstall

### Linux/Mac:
```bash
crontab -e
# Remove the line containing 'daily_update.py'
```

### Windows:
```cmd
schtasks /Delete /TN "TrackEco_DailyUpdate" /F
```


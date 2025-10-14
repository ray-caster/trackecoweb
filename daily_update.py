#!/usr/bin/env python3
"""
Daily Statistics Update Script
Updates plastic kg statistics daily at 8 PM WIB (1 PM UTC)
Increases impact_plastic_collected by a random float between 8-20
"""

import random
from datetime import datetime
from firebase_config import get_firestore_client, get_website_data, update_website_data

def update_daily_statistics():
    """Update the plastic collected statistics with random increment."""
    try:
        # Get current website data
        website_data = get_website_data()
        
        if not website_data:
            print("Error: Could not retrieve website data")
            return False
        
        # Get current stats
        current_stats = website_data.get('stats', {})
        current_plastic = current_stats.get('impact_plastic_collected', 3000)
        
        # Generate random increment between 8 and 20
        increment = round(random.uniform(8.0, 20.0), 2)
        
        # Calculate new value
        new_plastic = round(current_plastic + increment, 2)
        
        # Update stats
        current_stats['impact_plastic_collected'] = new_plastic
        website_data['stats'] = current_stats
        website_data['updated_at'] = datetime.now()
        
        # Save to database
        if update_website_data(website_data):
            print(f"✓ Successfully updated plastic collected: {current_plastic} kg → {new_plastic} kg (+{increment} kg)")
            print(f"  Updated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S WIB')}")
            return True
        else:
            print("✗ Failed to update website data")
            return False
            
    except Exception as e:
        print(f"✗ Error updating statistics: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("TrackEco Daily Statistics Update")
    print("=" * 60)
    update_daily_statistics()
    print("=" * 60)


# create_daily_branches.py
# Full path: /create_daily_branches.py

from datetime import datetime, timedelta
import subprocess
import sys

def create_branch(date, days_remaining):
    """Create and push a feature branch following GitFlow."""
    month = date.strftime('%b').lower()
    day = date.strftime('%d')
    branch_name = f"feature/{month}-{day}-{days_remaining}-days-to-CSCIE-94"
    
    try:
        # Ensure we're on main
        subprocess.run(['git', 'checkout', 'main'], check=True, capture_output=True)
        subprocess.run(['git', 'pull', 'origin', 'main'], check=True, capture_output=True)
        
        # Create branch
        subprocess.run(['git', 'checkout', '-b', branch_name], check=True, capture_output=True)
        
        # Push to remote with tracking
        subprocess.run(['git', 'push', '-u', 'origin', branch_name], check=True, capture_output=True)
        
        print(f"✓ Created: {branch_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {branch_name} - {e}")
        return False

def main():
    target_date = datetime(2026, 1, 26).date()
    today = datetime.now().date()
    
    # Calculate all dates from today to target
    current_date = today
    branches_created = 0
    
    while current_date <= target_date:
        days_remaining = (target_date - current_date).days
        
        if create_branch(current_date, days_remaining):
            branches_created += 1
        
        current_date += timedelta(days=1)
    
    print(f"\nTotal branches created: {branches_created}")
    
    # Return to main
    subprocess.run(['git', 'checkout', 'main'], check=True, capture_output=True)

if __name__ == "__main__":
    main()

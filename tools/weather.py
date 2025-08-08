import subprocess
import json
from typing import Dict, Any, Optional


def get_weather(location: str = "Tokyo") -> Dict[str, Any]:
    """Get current weather information using Mac Shortcuts.
    
    Args:
        location: Location name (city, region, etc.)
    
    Returns:
        Dictionary containing weather information from Shortcuts
    """
    try:
        # Run the Mac Shortcuts command with location as input
        result = subprocess.run(
            ["shortcuts", "run", "get-weather"],
            input=location,
            text=True,
            capture_output=True,
            check=True
        )
        
        # Try to parse the output as JSON
        try:
            weather_data = json.loads(result.stdout.strip())
            return weather_data
        except json.JSONDecodeError:
            # If not JSON, return as plain text
            return {
                "location": location,
                "weather_info": result.stdout.strip(),
                "source": "Mac Shortcuts"
            }
        
    except subprocess.CalledProcessError as e:
        return {
            "error": f"Shortcuts command failed: {e.stderr.strip() if e.stderr else str(e)}",
            "location": location
        }
    except FileNotFoundError:
        return {
            "error": "Shortcuts command not found. Make sure you're running on macOS with Shortcuts app installed.",
            "location": location
        }
    except Exception as e:
        return {
            "error": f"An error occurred: {str(e)}",
            "location": location
        }


def get_weather_forecast(location: str = "Tokyo") -> Dict[str, Any]:
    """Get weather forecast using Mac Shortcuts.
    
    Args:
        location: Location name (city, region, etc.)
    
    Returns:
        Dictionary containing forecast information from Shortcuts
    """
    try:
        # Run the Mac Shortcuts command for forecast
        result = subprocess.run(
            ["shortcuts", "run", "get-weather-forecast"],
            input=location,
            text=True,
            capture_output=True,
            check=True
        )
        
        # Try to parse the output as JSON
        try:
            forecast_data = json.loads(result.stdout.strip())
            return forecast_data
        except json.JSONDecodeError:
            # If not JSON, return as plain text
            return {
                "location": location,
                "forecast_info": result.stdout.strip(),
                "source": "Mac Shortcuts"
            }
        
    except subprocess.CalledProcessError as e:
        return {
            "error": f"Shortcuts command failed: {e.stderr.strip() if e.stderr else str(e)}",
            "location": location
        }
    except FileNotFoundError:
        return {
            "error": "Shortcuts command not found. Make sure you're running on macOS with Shortcuts app installed.",
            "location": location
        }
    except Exception as e:
        return {
            "error": f"An error occurred: {str(e)}",
            "location": location
        }
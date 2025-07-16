import os
import datetime
import typing
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials


SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def get_schedule(
    calendar_id: str = 'primary',
    days_ahead: int = 7,
    max_results: int = 10
) -> str:
    """
    Retrieve schedule from Google Calendar.
    
    Args:
        calendar_id: The calendar ID to retrieve events from (default: 'primary')
        days_ahead: Number of days ahead to retrieve events for (default: 7)
        max_results: Maximum number of events to return (default: 10)
    
    Returns:
        List of events.
    """
    try:
        service = get_service()
        
        # Calculate time range
        now = datetime.datetime.utcnow()
        time_min = now.isoformat() + 'Z'  # 'Z' indicates UTC time
        time_max = (now + datetime.timedelta(days=days_ahead)).isoformat() + 'Z'
        
        # Call the Calendar API
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            timeZone='Asia/Tokyo',
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        # Format events for easier consumption
        formatted_events = []
        for event in events:
            start = event.get('start', {})
            end = event.get('end', {})
            
            # Handle all-day events
            start_time = start.get('dateTime', start.get('date'))
            end_time = end.get('dateTime', end.get('date'))
            
            formatted_event = {
                'id': event.get('id'),
                'summary': event.get('summary', 'No title'),
                'description': event.get('description', ''),
                'start': start_time,
                'end': end_time,
                'location': event.get('location', ''),
                'attendees': [
                    {
                        'email': attendee.get('email'),
                        'name': attendee.get('displayName'),
                        'status': attendee.get('responseStatus')
                    }
                    for attendee in event.get('attendees', [])
                ],
                'creator': event.get('creator', {}),
                'organizer': event.get('organizer', {}),
                'status': event.get('status'),
                'html_link': event.get('htmlLink'),
                'hangout_link': event.get('hangoutLink'),
                'conference_data': event.get('conferenceData', {}),
                'is_all_day': 'date' in start
            }
            formatted_events.append(formatted_event)

        return f"{formatted_events}"

    except HttpError as error:
        print(f'An error occurred: {error}')
        raise
    except Exception as error:
        print(f'An unexpected error occurred: {error}')
        raise


def get_service():
    """credential.json → token.json → Generate Service"""
    creds: typing.Union[Credentials, None] = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credential.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)

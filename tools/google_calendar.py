import os
import datetime
import typing
import warnings
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials

# [WORK AROUND] Suppress Pydantic warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic.json_schema")

SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate():
    """Authenticate and return the Google Calendar API service."""
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

def get_schedule(
    calendar_id: str = 'primary',
    days_ahead: int = 7,
    max_results: int = 10
) -> str:
    """
    Retrieve schedule from Google Calendar.
    If you dont know calendar_id, you use `list_calendars()` to get the list of calendars, and you use calendar_id you got.
    
    Args:
        calendar_id: The calendar ID to retrieve events from (default: 'primary')
        days_ahead: Number of days ahead to retrieve events for (default: 7)
        max_results: Maximum number of events to return (default: 10)
    
    Returns:
        List of events.
    """
    try:
        service = authenticate()
        
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

def create_event(
    summary: str,
    start_time: str,
    end_time: str,
    description: str = '',
    location: str = '',
    calendar_id: str = 'primary',
    timezone: str = 'Asia/Tokyo'
):
    """
    Create a new event in Google Calendar. Return the created event details.
    
    Args:
        summary: Event title/summary
        start_time: Start time in ISO format (e.g., '2024-01-01T10:00:00')
        end_time: End time in ISO format (e.g., '2024-01-01T11:00:00')
        description: Event description (optional)
        location: Event location (optional)
        calendar_id: Calendar ID to create event in (default: 'primary')
        attendees: List of email addresses to invite (optional)
        timezone: Timezone for the event (default: 'Asia/Tokyo')
    """
    try:
        service = authenticate()
        
        # Prepare event data
        event = {
            'summary': summary,
            'description': description,
            'location': location,
            'start': {
                'dateTime': start_time,
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_time,
                'timeZone': timezone,
            },
        }
        
        # Create the event
        created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
        return created_event

    except HttpError as error:
        print(f'An error occurred: {error}')
        raise
    except Exception as error:
        print(f'An unexpected error occurred: {error}')
        raise


def update_event(
    event_id: str,
    summary: str = None,
    start_time: str = None,
    end_time: str = None,
    description: str = None,
    location: str = None,
    calendar_id: str = 'primary',
    attendees: typing.List[str] = None,
    timezone: str = 'Asia/Tokyo'
) -> str:
    """
    Update an existing event in Google Calendar. return the updated event details.
    
    Args:
        event_id: ID of the event to update
        summary: New event title/summary (optional)
        start_time: New start time in ISO format (optional)
        end_time: New end time in ISO format (optional)
        description: New event description (optional)
        location: New event location (optional)
        calendar_id: Calendar ID where the event exists (default: 'primary')
        attendees: New list of email addresses to invite (optional)
        timezone: Timezone for the event (default: 'Asia/Tokyo')
    """
    try:
        service = authenticate()
        
        # Get the existing event
        existing_event = service.events().get(
            calendarId=calendar_id,
            eventId=event_id
        ).execute()
        
        # Update only the provided fields
        if summary is not None:
            existing_event['summary'] = summary
        if description is not None:
            existing_event['description'] = description
        if location is not None:
            existing_event['location'] = location
        if start_time is not None:
            existing_event['start'] = {
                'dateTime': start_time,
                'timeZone': timezone,
            }
        if end_time is not None:
            existing_event['end'] = {
                'dateTime': end_time,
                'timeZone': timezone,
            }
        if attendees is not None:
            existing_event['attendees'] = [{'email': email} for email in attendees]
        
        # Update the event
        updated_event = service.events().update(calendarId=calendar_id, eventId=event_id, body=existing_event).execute()
        return updated_event
        
    except HttpError as error:
        print(f'An error occurred: {error}')
        raise
    except Exception as error:
        print(f'An unexpected error occurred: {error}')
        raise


def list_calendars(
    max_results: int = 100,
    min_access_role: str = None,
    show_deleted: bool = False,
    show_hidden: bool = False
) -> str:
    """
    Retrieve list of calendars from Google Calendar.

    Args:
        max_results: Maximum number of calendars to return (default: 100, max: 250)
        min_access_role: Minimum access role required (optional)
                        Options: 'freeBusyReader', 'owner', 'reader', 'writer'
        show_deleted: Include deleted calendar entries (default: False)
        show_hidden: Include hidden calendar entries (default: False)
    
    Returns:
        List of calendars with their details
    """
    try:
        service = authenticate()
        
        # Prepare request parameters
        params = {
            'maxResults': max_results,
            'showDeleted': show_deleted,
            'showHidden': show_hidden
        }
        
        if min_access_role:
            params['minAccessRole'] = min_access_role
        
        # Call the Calendar API
        calendar_list = service.calendarList().list(**params).execute()
        
        calendars = calendar_list.get('items', [])
        
        # Format calendars for easier consumption
        formatted_calendars = []
        for calendar in calendars:
            formatted_calendar = {
                'id': calendar.get('id'),
                'summary': calendar.get('summary'),
                'description': calendar.get('description', ''),
                'location': calendar.get('location', ''),
                'timezone': calendar.get('timeZone'),
                'access_role': calendar.get('accessRole'),
                'is_primary': calendar.get('primary', False),
                'is_selected': calendar.get('selected', False),
                'color_id': calendar.get('colorId'),
                'background_color': calendar.get('backgroundColor'),
                'foreground_color': calendar.get('foregroundColor'),
                'summary_override': calendar.get('summaryOverride'),
                'conference_properties': calendar.get('conferenceProperties', {}),
                'notification_settings': calendar.get('notificationSettings', {}),
                'default_reminders': calendar.get('defaultReminders', [])
            }
            formatted_calendars.append(formatted_calendar)
        
        return f"{formatted_calendars}"
        
    except HttpError as error:
        print(f'An error occurred: {error}')
        raise
    except Exception as error:
        print(f'An unexpected error occurred: {error}')
        raise

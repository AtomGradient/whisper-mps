#!/usr/bin/env python3
"""
YouTube Channel Video Parser
Extracts video URLs and titles from YouTube channel pages using yt-dlp.
"""

from typing import List, Dict, Optional
from pathlib import Path
import json
import sys
import argparse
import subprocess
import shutil


def check_ytdlp_installed() -> bool:
    """Check if yt-dlp is installed."""
    return shutil.which('yt-dlp') is not None


def fetch_videos_with_ytdlp(
    url: str, 
    cookies_file: Optional[str] = None,
    max_videos: Optional[int] = None
) -> List[Dict[str, str]]:
    """
    Fetch video information from YouTube channel using yt-dlp.
    
    Args:
        url: YouTube channel URL
        cookies_file: Path to cookies.txt file (optional)
        max_videos: Maximum number of videos to fetch (optional)
        
    Returns:
        List of dictionaries with video 'url' and 'title'
    """
    if not check_ytdlp_installed():
        print("Error: yt-dlp is not installed!")
        print("\nInstall it with:")
        print("  pip install yt-dlp")
        print("  # or")
        print("  pip3 install yt-dlp")
        sys.exit(1)
    
    # Build yt-dlp command
    cmd = [
        'yt-dlp',
        '--flat-playlist',  # Don't download, just get info
        '--print', '%(id)s|%(title)s',  # Custom output format
        '--no-warnings',
    ]
    
    # Add cookies if provided
    if cookies_file:
        if not Path(cookies_file).exists():
            print(f"Error: Cookies file '{cookies_file}' not found!")
            sys.exit(1)
        cmd.extend(['--cookies', cookies_file])
    
    # Add max videos limit
    if max_videos:
        cmd.extend(['--playlist-end', str(max_videos)])
    
    cmd.append(url)
    
    print(f"Fetching videos with yt-dlp...")
    if cookies_file:
        print(f"Using cookies from: {cookies_file}")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=120
        )
        
        # Parse output
        videos = []
        for line in result.stdout.strip().split('\n'):
            if '|' in line:
                video_id, title = line.split('|', 1)
                videos.append({
                    'url': f'https://www.youtube.com/watch?v={video_id}',
                    'title': title.strip()
                })
        
        return videos
        
    except subprocess.TimeoutExpired:
        print("Error: yt-dlp command timed out")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error running yt-dlp: {e}")
        print(f"stderr: {e.stderr}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


def save_to_json(videos: List[Dict[str, str]], output_path: str | Path = 'youtube_videos.json') -> None:
    """
    Save extracted videos to JSON file.
    
    Args:
        videos: List of video dictionaries
        output_path: Output file path
    """
    path = Path(output_path)
    path.write_text(
        json.dumps(videos, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )
    print(f"✓ Saved {len(videos)} videos to {output_path}")


def save_to_csv(videos: List[Dict[str, str]], output_path: str | Path = 'youtube_videos.csv') -> None:
    """
    Save extracted videos to CSV file.
    
    Args:
        videos: List of video dictionaries
        output_path: Output file path
    """
    import csv
    
    path = Path(output_path)
    with path.open('w', encoding='utf-8', newline='') as f:
        if videos:
            writer = csv.DictWriter(f, fieldnames=['url', 'title'])
            writer.writeheader()
            writer.writerows(videos)
    
    print(f"✓ Saved {len(videos)} videos to {output_path}")


def save_to_txt(videos: List[Dict[str, str]], output_path: str | Path = 'youtube_videos.txt') -> None:
    """
    Save extracted videos to plain text file.
    
    Args:
        videos: List of video dictionaries
        output_path: Output file path
    """
    path = Path(output_path)
    lines = []
    for video in videos:
        lines.append(f"{video['title']}")
        lines.append(f"{video['url']}")
        lines.append("")  # Empty line between videos
    
    path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"✓ Saved {len(videos)} videos to {output_path}")


def print_videos(videos: List[Dict[str, str]], limit: Optional[int] = None) -> None:
    """
    Print extracted videos to console.
    
    Args:
        videos: List of video dictionaries
        limit: Maximum number of videos to print (None for all)
    """
    total = len(videos)
    display_count = min(limit, total) if limit else total
    
    print(f"\n{'='*80}")
    print(f"Found {total} videos on the channel")
    print(f"{'='*80}\n")
    
    for i, video in enumerate(videos[:display_count], 1):
        print(f"{i}. {video['title']}")
        print(f"   {video['url']}\n")
    
    if limit and total > limit:
        print(f"... and {total - limit} more videos\n")


def main() -> None:
    """Command-line interface for YouTube channel parser."""
    parser = argparse.ArgumentParser(
        description='Parse YouTube channel pages to extract video URLs and titles using yt-dlp',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python youtube_parser.py https://www.youtube.com/@Nicholas_He/videos
  
  # With cookies for age-restricted or private content
  python youtube_parser.py https://www.youtube.com/@Nicholas_He/videos --cookies cookies.txt
  
  # Limit number of videos
  python youtube_parser.py https://www.youtube.com/@Nicholas_He/videos --max 50
  
  # Custom output formats
  python youtube_parser.py https://www.youtube.com/@Nicholas_He/videos -o my_videos.json
  python youtube_parser.py https://www.youtube.com/@Nicholas_He/videos --csv videos.csv
  python youtube_parser.py https://www.youtube.com/@Nicholas_He/videos --txt videos.txt
  
  # Multiple outputs
  python youtube_parser.py https://www.youtube.com/@Nicholas_He/videos -o data.json --csv data.csv --txt data.txt

How to get cookies.txt:
  1. Install browser extension "Get cookies.txt LOCALLY" (Chrome/Firefox)
  2. Go to youtube.com and log in
  3. Click the extension icon and export cookies
  4. Save as cookies.txt
        """
    )
    
    parser.add_argument(
        'url',
        help='YouTube channel URL (e.g., https://www.youtube.com/@ChannelName/videos)'
    )
    parser.add_argument(
        '-o', '--output',
        default='youtube_videos.json',
        help='Output JSON file path (default: youtube_videos.json)'
    )
    parser.add_argument(
        '--csv',
        help='Also save as CSV file'
    )
    parser.add_argument(
        '--txt',
        help='Also save as plain text file'
    )
    parser.add_argument(
        '-c', '--cookies',
        help='Path to cookies.txt file for authentication'
    )
    parser.add_argument(
        '-m', '--max',
        type=int,
        help='Maximum number of videos to fetch'
    )
    parser.add_argument(
        '-l', '--limit',
        type=int,
        help='Limit number of videos to display in console'
    )
    parser.add_argument(
        '--no-print',
        action='store_true',
        help='Do not print videos to console'
    )
    
    args = parser.parse_args()
    
    # Validate URL
    if not (args.url.startswith('http://') or args.url.startswith('https://')):
        print(f"Error: '{args.url}' is not a valid URL")
        print("URL should start with http:// or https://")
        sys.exit(1)
    
    # Fetch videos using yt-dlp
    videos = fetch_videos_with_ytdlp(
        args.url,
        cookies_file=args.cookies,
        max_videos=args.max
    )
    
    # Print results
    if not args.no_print:
        print_videos(videos, limit=args.limit)
    
    # Save to files
    if videos:
        save_to_json(videos, args.output)
        
        if args.csv:
            save_to_csv(videos, args.csv)
        
        if args.txt:
            save_to_txt(videos, args.txt)
    else:
        print("Warning: No videos found!")
        print("\nTroubleshooting:")
        print("- Make sure the URL is correct and includes /videos at the end")
        print("- Try using --cookies if the content requires authentication")
        print("- Check if the channel actually has videos")


if __name__ == "__main__":
    main()
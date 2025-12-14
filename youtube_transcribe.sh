#!/bin/bash

# YouTube Audio Download and Transcription Script
# Usage: ./youtube_transcribe.sh <json_file> [options]

set -e  # Exit on error

# Default values
JSON_FILE=""
USE_COOKIES=false
OUTPUT_DIR="./transcriptions"
AUDIO_DIR="./audios"
MODEL_NAME="large-v3"
SKIP_DOWNLOAD=false
SKIP_TRANSCRIBE=false
START_INDEX=1
END_INDEX=""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print usage
usage() {
    cat << EOF
Usage: $0 <json_file> [options]

Download YouTube videos as audio and transcribe them using Whisper.

Arguments:
    json_file           Path to JSON file with video URLs and titles (from youtube_parser.py)

Options:
    -c, --cookies           Use cookies from Chrome browser (via --cookies flag in ytdl-low)
    -o, --output-dir DIR    Output directory for transcriptions (default: ./transcriptions)
    -a, --audio-dir DIR     Output directory for audio files (default: ./audios)
    -m, --model NAME        Whisper model name (default: large-v3)
    --skip-download         Skip download, only transcribe existing audio files
    --skip-transcribe       Only download, skip transcription
    --start N               Start from video index N (default: 1)
    --end N                 End at video index N (default: all)
    -h, --help             Show this help message

Examples:
    # Basic usage
    $0 my_videos.json

    # With cookies from Chrome browser
    $0 my_videos.json --cookies

    # Custom directories
    $0 my_videos.json --audio-dir ./audio --output-dir ./texts

    # Process only videos 10-20
    $0 my_videos.json --start 10 --end 20

    # Only download (skip transcription)
    $0 my_videos.json --skip-transcribe

    # Only transcribe existing files
    $0 my_videos.json --skip-download

Note:
    The --cookies flag tells ytdl-low to use cookies from your Chrome browser.
    Make sure you're logged into YouTube in Chrome before using this option.

EOF
    exit 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -c|--cookies)
            USE_COOKIES=true
            shift
            ;;
        -o|--output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -a|--audio-dir)
            AUDIO_DIR="$2"
            shift 2
            ;;
        -m|--model)
            MODEL_NAME="$2"
            shift 2
            ;;
        --skip-download)
            SKIP_DOWNLOAD=true
            shift
            ;;
        --skip-transcribe)
            SKIP_TRANSCRIBE=true
            shift
            ;;
        --start)
            START_INDEX="$2"
            shift 2
            ;;
        --end)
            END_INDEX="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            if [[ -z "$JSON_FILE" ]]; then
                JSON_FILE="$1"
            else
                echo -e "${RED}Error: Unknown option: $1${NC}"
                usage
            fi
            shift
            ;;
    esac
done

# Validate JSON file
if [[ -z "$JSON_FILE" ]]; then
    echo -e "${RED}Error: JSON file is required${NC}"
    usage
fi

if [[ ! -f "$JSON_FILE" ]]; then
    echo -e "${RED}Error: JSON file '$JSON_FILE' not found${NC}"
    exit 1
fi

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if required commands/scripts exist
check_command() {
    if ! command -v "$1" &> /dev/null; then
        echo -e "${RED}Error: '$1' command not found${NC}"
        echo "Please install $1 first"
        exit 1
    fi
}

check_script() {
    if [[ ! -f "$1" ]]; then
        echo -e "${RED}Error: Script '$1' not found${NC}"
        exit 1
    fi
    if [[ ! -x "$1" ]]; then
        echo -e "${YELLOW}Warning: '$1' is not executable, making it executable...${NC}"
        chmod +x "$1"
    fi
}

# Determine paths for ytdl-low and whisper-mps
if [[ "$SKIP_DOWNLOAD" == false ]]; then
    # Check if ytdl-low exists locally first, otherwise use system command
    if [[ -f "$SCRIPT_DIR/ytdl-low" ]]; then
        YTDL_CMD="$SCRIPT_DIR/ytdl-low"
        check_script "$YTDL_CMD"
    else
        check_command "ytdl-low"
        YTDL_CMD="ytdl-low"
    fi
fi

if [[ "$SKIP_TRANSCRIBE" == false ]]; then
    # whisper-mps is a system command
    check_command "whisper-mps"
    WHISPER_CMD="whisper-mps"
fi

check_command "jq"

# Create directories
mkdir -p "$OUTPUT_DIR"
mkdir -p "$AUDIO_DIR"

# Function to sanitize filename (macOS compatible)
sanitize_filename() {
    # Remove or replace invalid characters, keep Chinese characters
    # Use perl instead of sed for better Unicode support on macOS
    echo "$1" | perl -pe 's/[\/\\:*?"<>|]/_/g' | cut -c1-200
}

# Read JSON and process videos
total_videos=$(jq length "$JSON_FILE")
echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}Found $total_videos videos in $JSON_FILE${NC}"
echo -e "${BLUE}================================================${NC}"

# Determine range
if [[ -z "$END_INDEX" ]]; then
    END_INDEX=$total_videos
fi

echo -e "${GREEN}Processing videos $START_INDEX to $END_INDEX${NC}\n"

# Counter for progress
success_count=0
fail_count=0

# Process each video
for ((i=$START_INDEX-1; i<$END_INDEX; i++)); do
    current=$((i + 1))
    
    # Extract video info using jq
    video_url=$(jq -r ".[$i].url" "$JSON_FILE")
    video_title=$(jq -r ".[$i].title" "$JSON_FILE")
    
    if [[ "$video_url" == "null" ]] || [[ -z "$video_url" ]]; then
        echo -e "${YELLOW}[$current/$END_INDEX] Skipping - no URL${NC}"
        continue
    fi
    
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}[$current/$END_INDEX] Processing: $video_title${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    # Sanitize title for filename
    safe_title=$(sanitize_filename "$video_title")
    audio_file="$AUDIO_DIR/${safe_title}.m4a"
    transcript_file="$OUTPUT_DIR/${safe_title}.txt"
    
    # Download audio
    if [[ "$SKIP_DOWNLOAD" == false ]]; then
        if [[ -f "$audio_file" ]]; then
            echo -e "${YELLOW}⊙ Audio file already exists, skipping download${NC}"
        else
            echo -e "${GREEN}⊙ Downloading audio...${NC}"
            
            # Build ytdl-low command
            if [[ "$USE_COOKIES" == true ]]; then
                if "$YTDL_CMD" --file-name "$audio_file" --cookies "$video_url"; then
                    echo -e "${GREEN}✓ Download successful${NC}"
                else
                    echo -e "${RED}✗ Download failed${NC}"
                    ((fail_count++))
                    continue
                fi
            else
                if "$YTDL_CMD" --file-name "$audio_file" "$video_url"; then
                    echo -e "${GREEN}✓ Download successful${NC}"
                else
                    echo -e "${RED}✗ Download failed${NC}"
                    ((fail_count++))
                    continue
                fi
            fi
        fi
    fi
    
    # Transcribe audio
    if [[ "$SKIP_TRANSCRIBE" == false ]]; then
        if [[ ! -f "$audio_file" ]]; then
            echo -e "${RED}✗ Audio file not found: $audio_file${NC}"
            ((fail_count++))
            continue
        fi
        
        if [[ -f "$transcript_file" ]]; then
            echo -e "${YELLOW}⊙ Transcript already exists, skipping transcription${NC}"
            ((success_count++))
        else
            echo -e "${GREEN}⊙ Transcribing audio...${NC}"
            
            if "$WHISPER_CMD" --file-name "$audio_file" --output-file-name "$transcript_file" --model-name "$MODEL_NAME"; then
                echo -e "${GREEN}✓ Transcription successful${NC}"
                ((success_count++))
            else
                echo -e "${RED}✗ Transcription failed${NC}"
                ((fail_count++))
            fi
        fi
    else
        ((success_count++))
    fi
    
    echo ""
done

# Summary
echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}Processing Complete${NC}"
echo -e "${BLUE}================================================${NC}"
echo -e "${GREEN}✓ Successful: $success_count${NC}"
if [[ $fail_count -gt 0 ]]; then
    echo -e "${RED}✗ Failed: $fail_count${NC}"
fi
echo -e "${BLUE}Audio files: $AUDIO_DIR${NC}"
echo -e "${BLUE}Transcripts: $OUTPUT_DIR${NC}"
echo -e "${BLUE}================================================${NC}"
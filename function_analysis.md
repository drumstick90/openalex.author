# JavaScript Functions Analysis - index.html

## Core Utility Functions
- `debugLog(message, data)` - Debug logging utility with console and UI output
- `safeExecute(fn, context)` - Error handling wrapper for all functions
- `addOutput(content, className)` - Display content in terminal
- `addTypedOutput(content, className, delay)` - Animated typing effect

## State Variables
- `isSearching` - Prevents concurrent searches (boolean)
- `currentResults` - Stores author search results (object)
- `awaitingSelection` - Author selection mode flag (boolean)  
- `selectedAuthor` - Currently selected author data (object)
- `inWorksMode` - Works analysis mode flag (boolean)
- `debugMode` - Debug logging enabled (boolean)

## Main Flow Functions
- `handleSelection(input)` - Author selection logic (1-5, y/n)
- `handleWorksQuery(input)` - Works command processing
- `performSearch(query)` - Author search API call
- `enterWorksMode()` - Switch to works analysis mode
- `promptForSelection()` - Ask user to select author

## API Integration Functions
- `getRecentWorks(authorId)` - Recent works API call
- `getTopCitedWorks(authorId)` - Top cited works API call  
- `searchWorks(authorId, searchTerm)` - Search within works
- `getWorksByYear(authorId, year)` - Filter works by year
- `getWorkStats(authorId)` - Publication statistics
- `getWorkTopics(authorId)` - Research topics analysis
- `showDebugInfo()` - Debug information display

## Display Functions
- `displayDetailedInfo(detailData)` - Format author profile
- `displayWorks(works, title)` - Format and display works list

## Event Handlers
- Input keypress handler for command processing
- Focus management for search input

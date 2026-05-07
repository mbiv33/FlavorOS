# Relationship Discovery Onboarding Integration

This directory contains prototype integration scaffolding for the Relationship Discovery Onboarding feature.

## Purpose

- Capture the planned integration points for FlavorOS
- Provide a low-risk code base for prototyping without modifying live folders
- Document how onboarding steps connect into the existing repository

## Integration responsibilities

- Authenticate email/calendar providers
- Extract contacts and participants
- Normalize contact data to the existing relationship schema
- Create or update `current.md`
- Support conversational validation and correction

## Next steps

1. Wire authorization flow to the desired email/calendar APIs
2. Implement data extraction and parsing
3. Map extracted contacts into `relationship-file-format.md`
4. Build the conversational validation step and output initializer

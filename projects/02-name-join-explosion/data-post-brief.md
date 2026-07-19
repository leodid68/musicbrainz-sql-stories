# Data Post Brief

## Purpose

**Audience:** Data practitioners, hiring teams, and analysts learning SQL
**Professional objective:** Demonstrate SQL reasoning, join-cardinality
validation, and concise communication
**Series and episode:** MusicBrainz SQL Stories #2
**Language:** Simple English

## Evidence

**Core question:** What happens when MusicBrainz artists are joined on their
exact primary name instead of a stable artist ID?
**Verified evidence:** 2,931,345 original rows; 5,379,621 joined rows;
2,448,276 cross-entity matches; 83.52% increase; Indigo example verified
**Reproduction path:** `analysis.sql`, `checks.sql`, and `claim-ledger.md`
**Dataset grain and snapshot:** One row per MusicBrainz artist entity,
2026-07-15 full export
**Limitation:** Controlled exact-name self-join; aliases excluded; different
MusicBrainz IDs do not prove different real-world people or groups

## Story

**Recommended hook:** A SQL query can run perfectly and still create the wrong
dataset.
**Main finding:** Joining on exact artist names increases the row count by
83.52% and creates 2,448,276 matches between different artist IDs.
**Technical lesson:** Validate input grain, join-key meaning, and expected
cardinality before trusting a join.
**Professional meaning:** Syntactic correctness is weaker than analytical
correctness.
**Previous episode:** Artist names are not identifiers; URL not yet confirmed
**Next episode:** Test the distinction between MusicBrainz tracks and
recordings

## Visual

**Format:** One static comparison chart
**Source data:** `original_artist_rows`, `name_join_rows`, and
`cross_entity_matches` from query 3 in `analysis.sql`
**Chart question:** How many rows exist before and after the exact-name join,
and how much of the increase comes from cross-entity matches?
**Accessibility text:** The original table contains 2.93 million artist rows.
Joining exact artist names produces 5.38 million rows, including 2.45 million
matches between different MusicBrainz artist IDs, an 83.52% increase.

## Publication Package

**Post text:** `linkedin-post.md`
**Repository link:** https://github.com/leodid68/musicbrainz-sql-stories/tree/main/projects/02-name-join-explosion
**Previous post link:** Add only after episode 1 has a confirmed publication
URL
**Next post preview:** Track versus recording identity in MusicBrainz
**Memory status:** ready for review

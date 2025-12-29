# PGA Tour GraphQL API - Complete Queries Reference

**Total Queries: 193**

---

## Table of Contents

- [adTagConfig](#adtagconfig)
- [allTimeRecordCategories](#alltimerecordcategories)
- [allTimeRecordStat](#alltimerecordstat)
- [alltoursponsors](#alltoursponsors)
- [aon](#aon)
- [articleAdConfig](#articleadconfig)
- [articleDetails](#articledetails)
- [articleDetailsCompressed](#articledetailscompressed)
- [broadcastTimes](#broadcasttimes)
- [bubble](#bubble)
- [bubbleWatch](#bubblewatch)
- [completeSchedule](#completeschedule)
- [contentFragmentTabs](#contentfragmenttabs)
- [contentFragmentType](#contentfragmenttype)
- [contentFragmentsCompressed](#contentfragmentscompressed)
- [courseHolesStats](#courseholesstats)
- [courseStats](#coursestats)
- [courseStatsDetails](#coursestatsdetails)
- [courseStatsOverview](#coursestatsoverview)
- [coverage](#coverage)
- [cupPastResults](#cuppastresults)
- [cupPlayOverviewLeaderboard](#cupplayoverviewleaderboard)
- [cupRoundLeaderboard](#cuproundleaderboard)
- [cupRoundLeaderboardCompressed](#cuproundleaderboardcompressed)
- [cupScorecard](#cupscorecard)
- [cupTeamRoster](#cupteamroster)
- [cupTeeTimes](#cupteetimes)
- [currentLeadersCompressed](#currentleaderscompressed)
- [defaultTourCup](#defaulttourcup)
- [eaglesForImpact](#eaglesforimpact)
- [eventGuideConfig](#eventguideconfig)
- [field](#field)
- [fieldStats](#fieldstats)
- [franchises](#franchises)
- [genericContent](#genericcontent)
- [genericContentCompressed](#genericcontentcompressed)
- [getExpertPicksTable](#getexpertpickstable)
- [getPowerRankingsTable](#getpowerrankingstable)
- [getRCPhotoGallery](#getrcphotogallery)
- [getRelatedFact](#getrelatedfact)
- [getShotCommentary](#getshotcommentary)
- [groupLocations](#grouplocations)
- [groupStageRankings](#groupstagerankings)
- [groupedField](#groupedfield)
- [historicalOdds](#historicalodds)
- [historicalScorecardStats](#historicalscorecardstats)
- [historicalTournamentsOdds](#historicaltournamentsodds)
- [holeDetails](#holedetails)
- [leaderboardCompressedV2](#leaderboardcompressedv2)
- [leaderboardCompressedV3](#leaderboardcompressedv3)
- [leaderboardHoleByHole](#leaderboardholebyhole)
- [leaderboardLegend](#leaderboardlegend)
- [leaderboardStats](#leaderboardstats)
- [leaderboardStrokes](#leaderboardstrokes)
- [leaderboardStrokesCompressed](#leaderboardstrokescompressed)
- [leaderboardV2](#leaderboardv2)
- [leaderboardV3](#leaderboardv3)
- [legalDocsCompressed](#legaldocscompressed)
- [liveAudioStream](#liveaudiostream)
- [liveVideoOverride](#livevideooverride)
- [matchOutcomeIq](#matchoutcomeiq)
- [matchPlayLeaderboard](#matchplayleaderboard)
- [matchPlayLeaderboardCompressed](#matchplayleaderboardcompressed)
- [matchPlayPlayoffScorecard](#matchplayplayoffscorecard)
- [matchPlayScorecard](#matchplayscorecard)
- [matchPlayScorecardResults](#matchplayscorecardresults)
- [matchPlayTeeTimes](#matchplayteetimes)
- [matchPlayTeeTimesCompressed](#matchplayteetimescompressed)
- [networks](#networks)
- [newletterSubscriptions](#newlettersubscriptions)
- [newsArticles](#newsarticles)
- [newsFranchises](#newsfranchises)
- [oddsGraph](#oddsgraph)
- [oddsTable](#oddstable)
- [oddsToWin](#oddstowin)
- [oddsToWinCompressed](#oddstowincompressed)
- [player](#player)
- [playerComparison](#playercomparison)
- [playerDirectory](#playerdirectory)
- [playerFinishStats](#playerfinishstats)
- [playerHub](#playerhub)
- [playerProfileCareer](#playerprofilecareer)
- [playerProfileCareerResults](#playerprofilecareerresults)
- [playerProfileCourseResults](#playerprofilecourseresults)
- [playerProfileMajorResults](#playerprofilemajorresults)
- [playerProfileOverview](#playerprofileoverview)
- [playerProfileScorecards](#playerprofilescorecards)
- [playerProfileSeasonResults](#playerprofileseasonresults)
- [playerProfileStandings](#playerprofilestandings)
- [playerProfileStats](#playerprofilestats)
- [playerProfileStatsFull](#playerprofilestatsfull)
- [playerProfileStatsFullV2](#playerprofilestatsfullv2)
- [playerProfileStatsYears](#playerprofilestatsyears)
- [playerProfileTournamentResults](#playerprofiletournamentresults)
- [playerSponsorships](#playersponsorships)
- [playerTournamentStatus](#playertournamentstatus)
- [players](#players)
- [playersOddsComparison](#playersoddscomparison)
- [playoffScorecard](#playoffscorecard)
- [playoffScorecardV2](#playoffscorecardv2)
- [playoffScorecardV3](#playoffscorecardv3)
- [playoffShotDetails](#playoffshotdetails)
- [playoffShotDetailsCompressed](#playoffshotdetailscompressed)
- [podcastEpisodes](#podcastepisodes)
- [podcasts](#podcasts)
- [presentedBy](#presentedby)
- [priorityRankings](#priorityrankings)
- [promoSection](#promosection)
- [rankingsWinners](#rankingswinners)
- [rsm](#rsm)
- [rsmLeaderboard](#rsmleaderboard)
- [ryderCupArticleDetailsCompressed](#rydercuparticledetailscompressed)
- [ryderCupBroadcastCoverage](#rydercupbroadcastcoverage)
- [ryderCupContentFragmentsCompressed](#rydercupcontentfragmentscompressed)
- [ryderCupContentOptions](#rydercupcontentoptions)
- [ryderCupContentPageTabs](#rydercupcontentpagetabs)
- [ryderCupMixedMedia](#rydercupmixedmedia)
- [ryderCupMixedMediaCompressed](#rydercupmixedmediacompressed)
- [ryderCupPlayerProfileCompressed](#rydercupplayerprofilecompressed)
- [ryderCupTeamRankings](#rydercupteamrankings)
- [ryderCupTeamRankingsCompressed](#rydercupteamrankingscompressed)
- [ryderCupTeamRankingsCompressedV2](#rydercupteamrankingscompressedv2)
- [ryderCupTeamRankingsV2](#rydercupteamrankingsv2)
- [ryderCupTournament](#rydercuptournament)
- [ryderCupTournaments](#rydercuptournaments)
- [ryderCupVideoById](#rydercupvideobyid)
- [scatterData](#scatterdata)
- [scatterDataCompressed](#scatterdatacompressed)
- [schedule](#schedule)
- [scheduleYears](#scheduleyears)
- [scorecardCompressedV3](#scorecardcompressedv3)
- [scorecardStats](#scorecardstats)
- [scorecardStatsComparison](#scorecardstatscomparison)
- [scorecardStatsV3](#scorecardstatsv3)
- [scorecardStatsV3Compressed](#scorecardstatsv3compressed)
- [scorecardV2](#scorecardv2)
- [scorecardV3](#scorecardv3)
- [searchBarFeatures](#searchbarfeatures)
- [searchPlayers](#searchplayers)
- [shotDetailsCompressedV3](#shotdetailscompressedv3)
- [shotDetailsV3](#shotdetailsv3)
- [signatureStandings](#signaturestandings)
- [sponsoredArticles](#sponsoredarticles)
- [sponsoredArticlesV2](#sponsoredarticlesv2)
- [sponsorships](#sponsorships)
- [statDetails](#statdetails)
- [statLeaders](#statleaders)
- [statOverview](#statoverview)
- [statsLeadersMobile](#statsleadersmobile)
- [teamStrokePlayLeaderboard](#teamstrokeplayleaderboard)
- [teamStrokePlayLeaderboardCompressed](#teamstrokeplayleaderboardcompressed)
- [teamStrokePlayScorecard](#teamstrokeplayscorecard)
- [teamStrokePlayScorecardRounds](#teamstrokeplayscorecardrounds)
- [teamStrokePlayTeeTimes](#teamstrokeplayteetimes)
- [teamStrokePlayTeeTimesCompressed](#teamstrokeplayteetimescompressed)
- [teeTimes](#teetimes)
- [teeTimesCompressed](#teetimescompressed)
- [teeTimesCompressedV2](#teetimescompressedv2)
- [teeTimesV2](#teetimesv2)
- [tglMatch](#tglmatch)
- [tglMatches](#tglmatches)
- [tglSchedule](#tglschedule)
- [tourCup](#tourcup)
- [tourCupCombined](#tourcupcombined)
- [tourCupSplit](#tourcupsplit)
- [tourCups](#tourcups)
- [tourcastTable](#tourcasttable)
- [tourcastVideos](#tourcastvideos)
- [tournamentGroupLocations](#tournamentgrouplocations)
- [tournamentHistory](#tournamenthistory)
- [tournamentOddsCompressedV2](#tournamentoddscompressedv2)
- [tournamentOddsToWin](#tournamentoddstowin)
- [tournamentOddsV2](#tournamentoddsv2)
- [tournamentOverview](#tournamentoverview)
- [tournamentPastResults](#tournamentpastresults)
- [tournamentRecap](#tournamentrecap)
- [tournaments](#tournaments)
- [tspPlayoffShotDetails](#tspplayoffshotdetails)
- [tspPlayoffShotDetailsCompressed](#tspplayoffshotdetailscompressed)
- [universityRankings](#universityrankings)
- [universityTotalPoints](#universitytotalpoints)
- [upcomingNetworks](#upcomingnetworks)
- [upcomingSchedule](#upcomingschedule)
- [videoById](#videobyid)
- [videoFranchises](#videofranchises)
- [videoHero](#videohero)
- [videoLandingPage](#videolandingpage)
- [videoNavigation](#videonavigation)
- [videoRecommendations](#videorecommendations)
- [videos](#videos)
- [weather](#weather)
- [yourTour](#yourtour)
- [yourTourNews](#yourtournews)

---

## adTagConfig

  Returns the AdConfig for the given optionally supplied tour and/or tournament

**⚠️ DEPRECATED:** use REST API

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tour` | `TourCode` | No |  |
| `tournamentId` | `String` | No |  |

### Returns

`AdConfig!` → [See AdConfig](./types/AdConfig.md)

### Example Query

```graphql
query {
  adTagConfig(tour: $tour, tournamentId: $tournamentId) {
    # ... fields
  }
}
```

---

## allTimeRecordCategories

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `TourCode!` | Yes |  |

### Returns

`AllTimeRecordCategories!` → [See AllTimeRecordCategories](./types/AllTimeRecordCategories.md)

### Example Query

```graphql
query {
  allTimeRecordCategories(tourCode: $tourCode) {
    # ... fields
  }
}
```

---

## allTimeRecordStat

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `TourCode!` | Yes |  |
| `recordId` | `String!` | Yes |  |

### Returns

`AllTimeRecordStat!` → [See AllTimeRecordStat](./types/AllTimeRecordStat.md)

### Example Query

```graphql
query {
  allTimeRecordStat(tourCode: $tourCode, recordId: $recordId) {
    # ... fields
  }
}
```

---

## alltoursponsors

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `TourCode!` | Yes |  |

### Returns

`[TourSponsor]!` → [See TourSponsor](./types/TourSponsor.md)

### Example Query

```graphql
query {
  alltoursponsors(tourCode: $tourCode) {
    # ... fields
  }
}
```

---

## aon

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `year` | `Int` | No |  |

### Returns

`Aon!` → [See Aon](./types/Aon.md)

### Example Query

```graphql
query {
  aon(year: $year) {
    # ... fields
  }
}
```

---

## articleAdConfig

**⚠️ DEPRECATED:** use REST API

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `franchise` | `String` | No |  |

### Returns

`AdTagConfig!` → [See AdTagConfig](./types/AdTagConfig.md)

### Example Query

```graphql
query {
  articleAdConfig(franchise: $franchise) {
    # ... fields
  }
}
```

---

## articleDetails

**⚠️ DEPRECATED:** Use articleDetailsCompressed

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `path` | `String!` | Yes |  |

### Returns

`NewsArticleDetails!` → [See NewsArticleDetails](./types/NewsArticleDetails.md)

### Example Query

```graphql
query {
  articleDetails(path: $path) {
    # ... fields
  }
}
```

---

## articleDetailsCompressed

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `path` | `String!` | Yes |  |

### Returns

`NewsArticleDetailsCompressed!` → [See NewsArticleDetailsCompressed](./types/NewsArticleDetailsCompressed.md)

### Example Query

```graphql
query {
  articleDetailsCompressed(path: $path) {
    # ... fields
  }
}
```

---

## broadcastTimes

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |
| `pastResults` | `Boolean` | No |  |

### Returns

`BroadcastCoverage!` → [See BroadcastCoverage](./types/BroadcastCoverage.md)

### Example Query

```graphql
query {
  broadcastTimes(tournamentId: $tournamentId, pastResults: $pastResults) {
    # ... fields
  }
}
```

---

## bubble

  Note this is optional on purpose

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `TourCode!` | Yes |  |
| `tournamentId` | `ID!` | Yes |  |

### Returns

`BubbleWatch` → [See BubbleWatch](./types/BubbleWatch.md)

### Example Query

```graphql
query {
  bubble(tourCode: $tourCode, tournamentId: $tournamentId) {
    # ... fields
  }
}
```

---

## bubbleWatch

**⚠️ DEPRECATED:** use bubble

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `TourCode!` | Yes |  |

### Returns

`TourCupRankingEvent` → [See TourCupRankingEvent](./types/TourCupRankingEvent.md)

### Example Query

```graphql
query {
  bubbleWatch(tourCode: $tourCode) {
    # ... fields
  }
}
```

---

## completeSchedule

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `TourCode!` | Yes |  |
| `filter` | `TournamentCategory` | No |  |

### Returns

`[Schedule!]!` → [See Schedule](./types/Schedule.md)

### Example Query

```graphql
query {
  completeSchedule(tourCode: $tourCode, filter: $filter) {
    # ... fields
  }
}
```

---

## contentFragmentTabs

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `path` | `String!` | Yes |  |

### Returns

`ContentFragmentTabs!` → [See ContentFragmentTabs](./types/ContentFragmentTabs.md)

### Example Query

```graphql
query {
  contentFragmentTabs(path: $path) {
    # ... fields
  }
}
```

---

## contentFragmentType

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `path` | `String!` | Yes |  |

### Returns

`ContentFragmentType` → [See ContentFragmentType](./types/ContentFragmentType.md)

### Example Query

```graphql
query {
  contentFragmentType(path: $path) {
    # ... fields
  }
}
```

---

## contentFragmentsCompressed

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `TourCode!` | Yes |  |
| `path` | `String` | No |  |
| `limit` | `Int` | No |  |
| `offset` | `Int` | No |  |

### Returns

`ContentFragmentsCompressed!` → [See ContentFragmentsCompressed](./types/ContentFragmentsCompressed.md)

### Example Query

```graphql
query {
  contentFragmentsCompressed(tourCode: $tourCode, path: $path, limit: $limit, offset: $offset) {
    # ... fields
  }
}
```

---

## courseHolesStats

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |
| `courseId` | `ID!` | Yes |  |

### Returns

`[HoleStatSummary!]!` → [See HoleStatSummary](./types/HoleStatSummary.md)

### Example Query

```graphql
query {
  courseHolesStats(tournamentId: $tournamentId, courseId: $courseId) {
    # ... fields
  }
}
```

---

## courseStats

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |

### Returns

`TournamentHoleStats!` → [See TournamentHoleStats](./types/TournamentHoleStats.md)

### Example Query

```graphql
query {
  courseStats(tournamentId: $tournamentId) {
    # ... fields
  }
}
```

---

## courseStatsDetails

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `TourCode!` | Yes |  |
| `round` | `ToughestRound` | No |  |
| `queryType` | `CourseStatsId!` | Yes |  |
| `year` | `Int` | No |  |

### Returns

`CourseStatsDetails!` → [See CourseStatsDetails](./types/CourseStatsDetails.md)

### Example Query

```graphql
query {
  courseStatsDetails(tourCode: $tourCode, round: $round, queryType: $queryType, year: $year) {
    # ... fields
  }
}
```

---

## courseStatsOverview

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `TourCode!` | Yes |  |
| `year` | `Int` | No |  |

### Returns

`CourseStatsOverview!` → [See CourseStatsOverview](./types/CourseStatsOverview.md)

### Example Query

```graphql
query {
  courseStatsOverview(tourCode: $tourCode, year: $year) {
    # ... fields
  }
}
```

---

## coverage

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |
| `pastResults` | `Boolean` | No |  |

### Returns

`BroadcastCoverage!` → [See BroadcastCoverage](./types/BroadcastCoverage.md)

### Example Query

```graphql
query {
  coverage(tournamentId: $tournamentId, pastResults: $pastResults) {
    # ... fields
  }
}
```

---

## cupPastResults

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |

### Returns

`CupPastResults!` → [See CupPastResults](./types/CupPastResults.md)

### Example Query

```graphql
query {
  cupPastResults(tournamentId: $tournamentId) {
    # ... fields
  }
}
```

---

## cupPlayOverviewLeaderboard

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`CupTournamentStatus!` → [See CupTournamentStatus](./types/CupTournamentStatus.md)

### Example Query

```graphql
query {
  cupPlayOverviewLeaderboard(id: $id) {
    # ... fields
  }
}
```

---

## cupRoundLeaderboard

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `String!` | Yes |  |
| `round` | `Int` | No |  |

### Returns

`CupTournamentLeaderboard!` → [See CupTournamentLeaderboard](./types/CupTournamentLeaderboard.md)

### Example Query

```graphql
query {
  cupRoundLeaderboard(tournamentId: $tournamentId, round: $round) {
    # ... fields
  }
}
```

---

## cupRoundLeaderboardCompressed

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `String!` | Yes |  |
| `round` | `Int` | No |  |

### Returns

`CupTournamentLeaderboardCompressed!` → [See CupTournamentLeaderboardCompressed](./types/CupTournamentLeaderboardCompressed.md)

### Example Query

```graphql
query {
  cupRoundLeaderboardCompressed(tournamentId: $tournamentId, round: $round) {
    # ... fields
  }
}
```

---

## cupScorecard

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |
| `round` | `Int!` | Yes |  |
| `matchId` | `Int!` | Yes |  |

### Returns

`CupScorecard!` → [See CupScorecard](./types/CupScorecard.md)

### Example Query

```graphql
query {
  cupScorecard(tournamentId: $tournamentId, round: $round, matchId: $matchId) {
    # ... fields
  }
}
```

---

## cupTeamRoster

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |

### Returns

`CupTeamRosters!` → [See CupTeamRosters](./types/CupTeamRosters.md)

### Example Query

```graphql
query {
  cupTeamRoster(tournamentId: $tournamentId) {
    # ... fields
  }
}
```

---

## cupTeeTimes

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |

### Returns

`CupTeeTimes!` → [See CupTeeTimes](./types/CupTeeTimes.md)

### Example Query

```graphql
query {
  cupTeeTimes(tournamentId: $tournamentId) {
    # ... fields
  }
}
```

---

## currentLeadersCompressed

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID` | No |  |
| `tourCode` | `TourCode` | No |  |

### Returns

`CurrentLeadersCompressed` → [See CurrentLeadersCompressed](./types/CurrentLeadersCompressed.md)

### Example Query

```graphql
query {
  currentLeadersCompressed(tournamentId: $tournamentId, tourCode: $tourCode) {
    # ... fields
  }
}
```

---

## defaultTourCup

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tour` | `TourCode!` | Yes |  |
| `year` | `Int` | No |  |

### Returns

`TourCupRankingEvent!` → [See TourCupRankingEvent](./types/TourCupRankingEvent.md)

### Example Query

```graphql
query {
  defaultTourCup(tour: $tour, year: $year) {
    # ... fields
  }
}
```

---

## eaglesForImpact

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |

### Returns

`EaglesForImpact!` → [See EaglesForImpact](./types/EaglesForImpact.md)

### Example Query

```graphql
query {
  eaglesForImpact(tournamentId: $tournamentId) {
    # ... fields
  }
}
```

---

## eventGuideConfig

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `String!` | Yes |  |

### Returns

`EventGuideConfig!` → [See EventGuideConfig](./types/EventGuideConfig.md)

### Example Query

```graphql
query {
  eventGuideConfig(tournamentId: $tournamentId) {
    # ... fields
  }
}
```

---

## field

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |
| `includeWithdrawn` | `Boolean` | No |  |
| `changesOnly` | `Boolean` | No |  |

### Returns

`Field!` → [See Field](./types/Field.md)

### Example Query

```graphql
query {
  field(id: $id, includeWithdrawn: $includeWithdrawn, changesOnly: $changesOnly) {
    # ... fields
  }
}
```

---

## fieldStats

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |
| `fieldStatType` | `FieldStatType` | No |  |

### Returns

`FieldStats!` → [See FieldStats](./types/FieldStats.md)

### Example Query

```graphql
query {
  fieldStats(tournamentId: $tournamentId, fieldStatType: $fieldStatType) {
    # ... fields
  }
}
```

---

## franchises

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `String` | No |  |

### Returns

`[String!]!` → [See String](./types/String.md)

### Example Query

```graphql
query {
  franchises(tourCode: $tourCode) {
    # ... fields
  }
}
```

---

## genericContent

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `path` | `String!` | Yes |  |

### Returns

`GenericContent!` → [See GenericContent](./types/GenericContent.md)

### Example Query

```graphql
query {
  genericContent(path: $path) {
    # ... fields
  }
}
```

---

## genericContentCompressed

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `path` | `String!` | Yes |  |

### Returns

`GenericContentCompressed!` → [See GenericContentCompressed](./types/GenericContentCompressed.md)

### Example Query

```graphql
query {
  genericContentCompressed(path: $path) {
    # ... fields
  }
}
```

---

## getExpertPicksTable

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `path` | `String!` | Yes |  |
| `year` | `Int` | No |  |

### Returns

`ExpertPicks!` → [See ExpertPicks](./types/ExpertPicks.md)

### Example Query

```graphql
query {
  getExpertPicksTable(path: $path, year: $year) {
    # ... fields
  }
}
```

---

## getPowerRankingsTable

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `path` | `String!` | Yes |  |

### Returns

`PowerRankings!` → [See PowerRankings](./types/PowerRankings.md)

### Example Query

```graphql
query {
  getPowerRankingsTable(path: $path) {
    # ... fields
  }
}
```

---

## getRCPhotoGallery

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `path` | `String!` | Yes |  |

### Returns

`RCPhotoGallery!` → [See RCPhotoGallery](./types/RCPhotoGallery.md)

### Example Query

```graphql
query {
  getRCPhotoGallery(path: $path) {
    # ... fields
  }
}
```

---

## getRelatedFact

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `path` | `String!` | Yes |  |

### Returns

`RelatedFact!` → [See RelatedFact](./types/RelatedFact.md)

### Example Query

```graphql
query {
  getRelatedFact(path: $path) {
    # ... fields
  }
}
```

---

## getShotCommentary

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `String!` | Yes |  |
| `playerId` | `String!` | Yes |  |
| `round` | `Int!` | Yes |  |

### Returns

`ShotCommentary!` → [See ShotCommentary](./types/ShotCommentary.md)

### Example Query

```graphql
query {
  getShotCommentary(tournamentId: $tournamentId, playerId: $playerId, round: $round) {
    # ... fields
  }
}
```

---

## groupLocations

  Returns full details for a match based on supplied matchId

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |
| `round` | `Int!` | Yes |  |

### Returns

`GroupLocation!` → [See GroupLocation](./types/GroupLocation.md)

### Example Query

```graphql
query {
  groupLocations(tournamentId: $tournamentId, round: $round) {
    # ... fields
  }
}
```

---

## groupStageRankings

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |

### Returns

`GroupStageRankings!` → [See GroupStageRankings](./types/GroupStageRankings.md)

### Example Query

```graphql
query {
  groupStageRankings(tournamentId: $tournamentId) {
    # ... fields
  }
}
```

---

## groupedField

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |
| `includeWithdrawn` | `Boolean` | No |  |
| `changesOnly` | `Boolean` | No |  |

### Returns

`GroupedField!` → [See GroupedField](./types/GroupedField.md)

### Example Query

```graphql
query {
  groupedField(id: $id, includeWithdrawn: $includeWithdrawn, changesOnly: $changesOnly) {
    # ... fields
  }
}
```

---

## historicalOdds

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `playerId` | `String!` | Yes |  |
| `tournamentId` | `String!` | Yes |  |
| `marketId` | `HistoricalOddsId!` | Yes |  |
| `timeStamp` | `AWSDateTime` | No |  |

### Returns

`HistoricalPlayerOdds` → [See HistoricalPlayerOdds](./types/HistoricalPlayerOdds.md)

### Example Query

```graphql
query {
  historicalOdds(playerId: $playerId, tournamentId: $tournamentId, marketId: $marketId, timeStamp: $timeStamp) {
    # ... fields
  }
}
```

---

## historicalScorecardStats

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `playerId` | `ID!` | Yes |  |

### Returns

`HistoricalPlayerScorecards!` → [See HistoricalPlayerScorecards](./types/HistoricalPlayerScorecards.md)

### Example Query

```graphql
query {
  historicalScorecardStats(playerId: $playerId) {
    # ... fields
  }
}
```

---

## historicalTournamentsOdds

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `String!` | Yes |  |
| `marketId` | `OddsMarketType!` | Yes |  |
| `timeStamp` | `AWSDateTime` | No |  |

### Returns

`HistoricalTournamentOdds` → [See HistoricalTournamentOdds](./types/HistoricalTournamentOdds.md)

### Example Query

```graphql
query {
  historicalTournamentsOdds(tournamentId: $tournamentId, marketId: $marketId, timeStamp: $timeStamp) {
    # ... fields
  }
}
```

---

## holeDetails

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |
| `courseId` | `ID!` | Yes |  |
| `hole` | `Int!` | Yes |  |

### Returns

`HoleDetail!` → [See HoleDetail](./types/HoleDetail.md)

### Example Query

```graphql
query {
  holeDetails(tournamentId: $tournamentId, courseId: $courseId, hole: $hole) {
    # ... fields
  }
}
```

---

## leaderboardCompressedV2

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`LeaderboardCompressedV2!` → [See LeaderboardCompressedV2](./types/LeaderboardCompressedV2.md)

### Example Query

```graphql
query {
  leaderboardCompressedV2(id: $id) {
    # ... fields
  }
}
```

---

## leaderboardCompressedV3

  Get the leaderboard for a tournament by tournamentID. The data in the payload property will be Base64 encoded.

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`LeaderboardCompressedV3!` → [See LeaderboardCompressedV3](./types/LeaderboardCompressedV3.md)

### Example Query

```graphql
query {
  leaderboardCompressedV3(id: $id) {
    # ... fields
  }
}
```

---

## leaderboardHoleByHole

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |
| `round` | `Int` | No |  |

### Returns

`LeaderboardHoleByHole!` → [See LeaderboardHoleByHole](./types/LeaderboardHoleByHole.md)

### Example Query

```graphql
query {
  leaderboardHoleByHole(tournamentId: $tournamentId, round: $round) {
    # ... fields
  }
}
```

---

## leaderboardLegend

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |
| `odds` | `Boolean!` | Yes |  |

### Returns

`LeaderboardInfo!` → [See LeaderboardInfo](./types/LeaderboardInfo.md)

### Example Query

```graphql
query {
  leaderboardLegend(tournamentId: $tournamentId, odds: $odds) {
    # ... fields
  }
}
```

---

## leaderboardStats

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |
| `statsType` | `LeaderboardStatsType` | No |  |

### Returns

`LeaderboardStats!` → [See LeaderboardStats](./types/LeaderboardStats.md)

### Example Query

```graphql
query {
  leaderboardStats(id: $id, statsType: $statsType) {
    # ... fields
  }
}
```

---

## leaderboardStrokes

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`LeaderboardStrokes!` → [See LeaderboardStrokes](./types/LeaderboardStrokes.md)

### Example Query

```graphql
query {
  leaderboardStrokes(id: $id) {
    # ... fields
  }
}
```

---

## leaderboardStrokesCompressed

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`LeaderboardStrokesCompressed!` → [See LeaderboardStrokesCompressed](./types/LeaderboardStrokesCompressed.md)

### Example Query

```graphql
query {
  leaderboardStrokesCompressed(id: $id) {
    # ... fields
  }
}
```

---

## leaderboardV2

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`LeaderboardV2!` → [See LeaderboardV2](./types/LeaderboardV2.md)

### Example Query

```graphql
query {
  leaderboardV2(id: $id) {
    # ... fields
  }
}
```

---

## leaderboardV3

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`LeaderboardV3!` → [See LeaderboardV3](./types/LeaderboardV3.md)

### Example Query

```graphql
query {
  leaderboardV3(id: $id) {
    # ... fields
  }
}
```

---

## legalDocsCompressed

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `path` | `String!` | Yes |  |

### Returns

`GenericContentCompressed!` → [See GenericContentCompressed](./types/GenericContentCompressed.md)

### Example Query

```graphql
query {
  legalDocsCompressed(path: $path) {
    # ... fields
  }
}
```

---

## liveAudioStream

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`AudioStream!` → [See AudioStream](./types/AudioStream.md)

### Example Query

```graphql
query {
  liveAudioStream(id: $id) {
    # ... fields
  }
}
```

---

## liveVideoOverride

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `TourCode!` | Yes |  |
| `tournamentId` | `String!` | Yes |  |

### Returns

`LiveVideoOverride!` → [See LiveVideoOverride](./types/LiveVideoOverride.md)

### Example Query

```graphql
query {
  liveVideoOverride(tourCode: $tourCode, tournamentId: $tournamentId) {
    # ... fields
  }
}
```

---

## matchOutcomeIq

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `String!` | Yes |  |
| `matchId` | `Int!` | Yes |  |
| `roundNumber` | `Int` | No |  |

### Returns

`RyderCupMatchOutcomeIQ!` → [See RyderCupMatchOutcomeIQ](./types/RyderCupMatchOutcomeIQ.md)

### Example Query

```graphql
query {
  matchOutcomeIq(tournamentId: $tournamentId, matchId: $matchId, roundNumber: $roundNumber) {
    # ... fields
  }
}
```

---

## matchPlayLeaderboard

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`MPLeaderboard!` → [See MPLeaderboard](./types/MPLeaderboard.md)

### Example Query

```graphql
query {
  matchPlayLeaderboard(id: $id) {
    # ... fields
  }
}
```

---

## matchPlayLeaderboardCompressed

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`LeaderboardCompressed!` → [See LeaderboardCompressed](./types/LeaderboardCompressed.md)

### Example Query

```graphql
query {
  matchPlayLeaderboardCompressed(id: $id) {
    # ... fields
  }
}
```

---

## matchPlayPlayoffScorecard

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |
| `roundNum` | `Int!` | Yes |  |
| `matchId` | `ID!` | Yes |  |

### Returns

`MPPlayoffScorecard!` → [See MPPlayoffScorecard](./types/MPPlayoffScorecard.md)

### Example Query

```graphql
query {
  matchPlayPlayoffScorecard(tournamentId: $tournamentId, roundNum: $roundNum, matchId: $matchId) {
    # ... fields
  }
}
```

---

## matchPlayScorecard

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |
| `roundNum` | `Int!` | Yes |  |
| `matchId` | `ID!` | Yes |  |

### Returns

`MPScorecard!` → [See MPScorecard](./types/MPScorecard.md)

### Example Query

```graphql
query {
  matchPlayScorecard(tournamentId: $tournamentId, roundNum: $roundNum, matchId: $matchId) {
    # ... fields
  }
}
```

---

## matchPlayScorecardResults

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |
| `roundNum` | `Int!` | Yes |  |
| `matchId` | `ID!` | Yes |  |

### Returns

`MPScorecardResults!` → [See MPScorecardResults](./types/MPScorecardResults.md)

### Example Query

```graphql
query {
  matchPlayScorecardResults(tournamentId: $tournamentId, roundNum: $roundNum, matchId: $matchId) {
    # ... fields
  }
}
```

---

## matchPlayTeeTimes

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |

### Returns

`MPTeeTimes!` → [See MPTeeTimes](./types/MPTeeTimes.md)

### Example Query

```graphql
query {
  matchPlayTeeTimes(tournamentId: $tournamentId) {
    # ... fields
  }
}
```

---

## matchPlayTeeTimesCompressed

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |

### Returns

`TeeTimesCompressed!` → [See TeeTimesCompressed](./types/TeeTimesCompressed.md)

### Example Query

```graphql
query {
  matchPlayTeeTimesCompressed(tournamentId: $tournamentId) {
    # ... fields
  }
}
```

---

## networks

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |

### Returns

`BroadcastNetworks!` → [See BroadcastNetworks](./types/BroadcastNetworks.md)

### Example Query

```graphql
query {
  networks(tournamentId: $tournamentId) {
    # ... fields
  }
}
```

---

## newletterSubscriptions

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `includeTournaments` | `Boolean` | No |  |

### Returns

`[Newsletter!]!` → [See Newsletter](./types/Newsletter.md)

### Example Query

```graphql
query {
  newletterSubscriptions(includeTournaments: $includeTournaments) {
    # ... fields
  }
}
```

---

## newsArticles

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tour` | `TourCode` | No |  |
| `franchise` | `String` | No |  |
| `franchises` | `[String!]` | No |  |
| `playerId` | `ID` | No |  |
| `playerIds` | `[ID!]` | No |  |
| `limit` | `Int` | No |  |
| `offset` | `Int` | No |  |
| `tags` | `[String!]` | No |  |
| `tournamentNum` | `String` | No |  |
| `targetYear` | `String` | No |  |
| `sectionName` | `String` | No |  |

### Returns

`NewsArticles!` → [See NewsArticles](./types/NewsArticles.md)

### Example Query

```graphql
query {
  newsArticles(tour: $tour, franchise: $franchise, franchises: $franchises, playerId: $playerId, playerIds: $playerIds, limit: $limit, offset: $offset, tags: $tags, tournamentNum: $tournamentNum, targetYear: $targetYear, sectionName: $sectionName) {
    # ... fields
  }
}
```

---

## newsFranchises

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `String` | No |  |
| `allFranchises` | `Boolean` | No |  |

### Returns

`[NewsFranchise!]!` → [See NewsFranchise](./types/NewsFranchise.md)

### Example Query

```graphql
query {
  newsFranchises(tourCode: $tourCode, allFranchises: $allFranchises) {
    # ... fields
  }
}
```

---

## oddsGraph

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `String!` | Yes |  |
| `playerIds` | `[String!]!` | Yes |  |
| `oddsTimeType` | `OddsTimeType` | No |  |
| `marketId` | `HistoricalOddsId` | No |  |
| `round` | `Int` | No |  |

### Returns

`OddsTimeline!` → [See OddsTimeline](./types/OddsTimeline.md)

### Example Query

```graphql
query {
  oddsGraph(tournamentId: $tournamentId, playerIds: $playerIds, oddsTimeType: $oddsTimeType, marketId: $marketId, round: $round) {
    # ... fields
  }
}
```

---

## oddsTable

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `String!` | Yes |  |
| `tournamentName` | `String!` | Yes |  |
| `markets` | `[ArticleOddsMarketsInput!]` | No |  |
| `players` | `[ArticleOddsPlayerInput!]` | No |  |
| `timeStamp` | `String` | No |  |

### Returns

`OddsTable!` → [See OddsTable](./types/OddsTable.md)

### Example Query

```graphql
query {
  oddsTable(tournamentId: $tournamentId, tournamentName: $tournamentName, markets: $markets, players: $players, timeStamp: $timeStamp) {
    # ... fields
  }
}
```

---

## oddsToWin

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `oddsToWinId` | `ID!` | Yes |  |

### Returns

`OddsToWinMarket!` → [See OddsToWinMarket](./types/OddsToWinMarket.md)

### Example Query

```graphql
query {
  oddsToWin(oddsToWinId: $oddsToWinId) {
    # ... fields
  }
}
```

---

## oddsToWinCompressed

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `oddsToWinId` | `ID!` | Yes |  |

### Returns

`OddsToWinMarketCompressed!` → [See OddsToWinMarketCompressed](./types/OddsToWinMarketCompressed.md)

### Example Query

```graphql
query {
  oddsToWinCompressed(oddsToWinId: $oddsToWinId) {
    # ... fields
  }
}
```

---

## player

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`PlayerBioWrapper!` → [See PlayerBioWrapper](./types/PlayerBioWrapper.md)

### Example Query

```graphql
query {
  player(id: $id) {
    # ... fields
  }
}
```

---

## playerComparison

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `TourCode!` | Yes |  |
| `playerIds` | `[String!]!` | Yes |  |
| `category` | `PlayerComparisonCategory` | No |  |
| `year` | `Int` | No |  |
| `tournamentId` | `String` | No |  |

### Returns

`PlayerComparison!` → [See PlayerComparison](./types/PlayerComparison.md)

### Example Query

```graphql
query {
  playerComparison(tourCode: $tourCode, playerIds: $playerIds, category: $category, year: $year, tournamentId: $tournamentId) {
    # ... fields
  }
}
```

---

## playerDirectory

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `TourCode!` | Yes |  |
| `active` | `Boolean` | No |  |

### Returns

`PlayerDirectory!` → [See PlayerDirectory](./types/PlayerDirectory.md)

### Example Query

```graphql
query {
  playerDirectory(tourCode: $tourCode, active: $active) {
    # ... fields
  }
}
```

---

## playerFinishStats

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `playerId` | `ID!` | Yes |  |
| `statId` | `String!` | Yes |  |
| `tourCode` | `TourCode!` | Yes |  |

### Returns

`PlayerFinishStats` → [See PlayerFinishStats](./types/PlayerFinishStats.md)

### Example Query

```graphql
query {
  playerFinishStats(playerId: $playerId, statId: $statId, tourCode: $tourCode) {
    # ... fields
  }
}
```

---

## playerHub

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `playerId` | `ID!` | Yes |  |

### Returns

`PlayerHubPlayerCompressed` → [See PlayerHubPlayerCompressed](./types/PlayerHubPlayerCompressed.md)

### Example Query

```graphql
query {
  playerHub(playerId: $playerId) {
    # ... fields
  }
}
```

---

## playerProfileCareer

**⚠️ DEPRECATED:** use REST API

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `playerId` | `String!` | Yes |  |
| `tourCode` | `TourCode` | No |  |

### Returns

`PlayerProfileCareer!` → [See PlayerProfileCareer](./types/PlayerProfileCareer.md)

### Example Query

```graphql
query {
  playerProfileCareer(playerId: $playerId, tourCode: $tourCode) {
    # ... fields
  }
}
```

---

## playerProfileCareerResults

**⚠️ DEPRECATED:** use REST API

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `playerId` | `ID!` | Yes |  |

### Returns

`PlayerProfileCareerResults!` → [See PlayerProfileCareerResults](./types/PlayerProfileCareerResults.md)

### Example Query

```graphql
query {
  playerProfileCareerResults(playerId: $playerId) {
    # ... fields
  }
}
```

---

## playerProfileCourseResults

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `playerId` | `String!` | Yes |  |
| `tourCode` | `TourCode` | No |  |

### Returns

`PlayerProfileCourseResults` → [See PlayerProfileCourseResults](./types/PlayerProfileCourseResults.md)

### Example Query

```graphql
query {
  playerProfileCourseResults(playerId: $playerId, tourCode: $tourCode) {
    # ... fields
  }
}
```

---

## playerProfileMajorResults

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `playerId` | `String!` | Yes |  |

### Returns

`PlayerProfileMajors` → [See PlayerProfileMajors](./types/PlayerProfileMajors.md)

### Example Query

```graphql
query {
  playerProfileMajorResults(playerId: $playerId) {
    # ... fields
  }
}
```

---

## playerProfileOverview

**⚠️ DEPRECATED:** use REST API

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `playerId` | `ID!` | Yes |  |
| `currentTour` | `TourCode` | No |  |

### Returns

`ProfileOverview!` → [See ProfileOverview](./types/ProfileOverview.md)

### Example Query

```graphql
query {
  playerProfileOverview(playerId: $playerId, currentTour: $currentTour) {
    # ... fields
  }
}
```

---

## playerProfileScorecards

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `playerId` | `ID!` | Yes |  |

### Returns

`HistoricalPlayerScorecards!` → [See HistoricalPlayerScorecards](./types/HistoricalPlayerScorecards.md)

### Example Query

```graphql
query {
  playerProfileScorecards(playerId: $playerId) {
    # ... fields
  }
}
```

---

## playerProfileSeasonResults

**⚠️ DEPRECATED:** use REST API

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `playerId` | `ID!` | Yes |  |
| `tourCode` | `TourCode` | No |  |
| `year` | `Int` | No |  |

### Returns

`PlayerResults!` → [See PlayerResults](./types/PlayerResults.md)

### Example Query

```graphql
query {
  playerProfileSeasonResults(playerId: $playerId, tourCode: $tourCode, year: $year) {
    # ... fields
  }
}
```

---

## playerProfileStandings

**⚠️ DEPRECATED:** use REST API

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `playerId` | `ID!` | Yes |  |

### Returns

`[PlayerOverviewStandings!]!` → [See PlayerOverviewStandings](./types/PlayerOverviewStandings.md)

### Example Query

```graphql
query {
  playerProfileStandings(playerId: $playerId) {
    # ... fields
  }
}
```

---

## playerProfileStats

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `playerId` | `ID!` | Yes |  |

### Returns

`[PlayerProfileStat!]!` → [See PlayerProfileStat](./types/PlayerProfileStat.md)

### Example Query

```graphql
query {
  playerProfileStats(playerId: $playerId) {
    # ... fields
  }
}
```

---

## playerProfileStatsFull

**⚠️ DEPRECATED:** use REST API

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `playerId` | `ID!` | Yes |  |
| `year` | `Int` | No |  |

### Returns

`[PlayerProfileStatFull!]!` → [See PlayerProfileStatFull](./types/PlayerProfileStatFull.md)

### Example Query

```graphql
query {
  playerProfileStatsFull(playerId: $playerId, year: $year) {
    # ... fields
  }
}
```

---

## playerProfileStatsFullV2

**⚠️ DEPRECATED:** use REST API

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `playerId` | `ID!` | Yes |  |
| `year` | `Int` | No |  |

### Returns

`PlayerProfileStatsFullV2!` → [See PlayerProfileStatsFullV2](./types/PlayerProfileStatsFullV2.md)

### Example Query

```graphql
query {
  playerProfileStatsFullV2(playerId: $playerId, year: $year) {
    # ... fields
  }
}
```

---

## playerProfileStatsYears

**⚠️ DEPRECATED:** use REST API

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `playerId` | `ID!` | Yes |  |

### Returns

`[PlayerProfileStatYear!]!` → [See PlayerProfileStatYear](./types/PlayerProfileStatYear.md)

### Example Query

```graphql
query {
  playerProfileStatsYears(playerId: $playerId) {
    # ... fields
  }
}
```

---

## playerProfileTournamentResults

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `playerId` | `ID!` | Yes |  |
| `tourCode` | `TourCode` | No |  |

### Returns

`PlayerProfileTournamentResults!` → [See PlayerProfileTournamentResults](./types/PlayerProfileTournamentResults.md)

### Example Query

```graphql
query {
  playerProfileTournamentResults(playerId: $playerId, tourCode: $tourCode) {
    # ... fields
  }
}
```

---

## playerSponsorships

**⚠️ DEPRECATED:** use REST API

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tour` | `TourCode!` | Yes |  |
| `sponsors` | `[PlayerSponsorBrand!]` | No |  |

### Returns

`[PlayerSponsorship!]!` → [See PlayerSponsorship](./types/PlayerSponsorship.md)

### Example Query

```graphql
query {
  playerSponsorships(tour: $tour, sponsors: $sponsors) {
    # ... fields
  }
}
```

---

## playerTournamentStatus

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `playerId` | `ID!` | Yes |  |

### Returns

`PlayerTournamentStatus` → [See PlayerTournamentStatus](./types/PlayerTournamentStatus.md)

### Example Query

```graphql
query {
  playerTournamentStatus(playerId: $playerId) {
    # ... fields
  }
}
```

---

## players

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ids` | `[ID!]!` | Yes |  |

### Returns

`[PlayerBioWrapper!]!` → [See PlayerBioWrapper](./types/PlayerBioWrapper.md)

### Example Query

```graphql
query {
  players(ids: $ids) {
    # ... fields
  }
}
```

---

## playersOddsComparison

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `playerIds` | `[String!]!` | Yes |  |

### Returns

`[PlayerComparisonOdds!]!` → [See PlayerComparisonOdds](./types/PlayerComparisonOdds.md)

### Example Query

```graphql
query {
  playersOddsComparison(playerIds: $playerIds) {
    # ... fields
  }
}
```

---

## playoffScorecard

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`PlayoffScorecard!` → [See PlayoffScorecard](./types/PlayoffScorecard.md)

### Example Query

```graphql
query {
  playoffScorecard(id: $id) {
    # ... fields
  }
}
```

---

## playoffScorecardV2

**⚠️ DEPRECATED:** use v3

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`[PlayoffScorecard!]` → [See PlayoffScorecard](./types/PlayoffScorecard.md)

### Example Query

```graphql
query {
  playoffScorecardV2(id: $id) {
    # ... fields
  }
}
```

---

## playoffScorecardV3

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |

### Returns

`TournamentPlayoffScorecards!` → [See TournamentPlayoffScorecards](./types/TournamentPlayoffScorecards.md)

### Example Query

```graphql
query {
  playoffScorecardV3(tournamentId: $tournamentId) {
    # ... fields
  }
}
```

---

## playoffShotDetails

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |
| `includeRadar` | `Boolean` | No |  |

### Returns

`GroupShotDetails!` → [See GroupShotDetails](./types/GroupShotDetails.md)

### Example Query

```graphql
query {
  playoffShotDetails(tournamentId: $tournamentId, includeRadar: $includeRadar) {
    # ... fields
  }
}
```

---

## playoffShotDetailsCompressed

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |
| `includeRadar` | `Boolean` | No |  |

### Returns

`GroupShotDetailsCompressed!` → [See GroupShotDetailsCompressed](./types/GroupShotDetailsCompressed.md)

### Example Query

```graphql
query {
  playoffShotDetailsCompressed(tournamentId: $tournamentId, includeRadar: $includeRadar) {
    # ... fields
  }
}
```

---

## podcastEpisodes

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `podcastId` | `String!` | Yes |  |
| `limit` | `Int` | No |  |
| `offset` | `Int` | No |  |

### Returns

`[Episode!]!` → [See Episode](./types/Episode.md)

### Example Query

```graphql
query {
  podcastEpisodes(podcastId: $podcastId, limit: $limit, offset: $offset) {
    # ... fields
  }
}
```

---

## podcasts

### Arguments

None

### Returns

`[Audio!]!` → [See Audio](./types/Audio.md)

### Example Query

```graphql
query {
  podcasts {
    # ... fields
  }
}
```

---

## presentedBy

### Arguments

None

### Returns

`PresentedByConfig!` → [See PresentedByConfig](./types/PresentedByConfig.md)

### Example Query

```graphql
query {
  presentedBy {
    # ... fields
  }
}
```

---

## priorityRankings

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `TourCode!` | Yes |  |
| `year` | `Int` | No |  |

### Returns

`PriorityRankings!` → [See PriorityRankings](./types/PriorityRankings.md)

### Example Query

```graphql
query {
  priorityRankings(tourCode: $tourCode, year: $year) {
    # ... fields
  }
}
```

---

## promoSection

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `section` | `PromoSectionType!` | Yes |  |

### Returns

`PromoSectionContainer!` → [See PromoSectionContainer](./types/PromoSectionContainer.md)

### Example Query

```graphql
query {
  promoSection(section: $section) {
    # ... fields
  }
}
```

---

## rankingsWinners

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `TourCode` | No |  |

### Returns

`[RankingsPastWinner!]!` → [See RankingsPastWinner](./types/RankingsPastWinner.md)

### Example Query

```graphql
query {
  rankingsWinners(tourCode: $tourCode) {
    # ... fields
  }
}
```

---

## rsm

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `year` | `Int` | No |  |

### Returns

`RSMStandings!` → [See RSMStandings](./types/RSMStandings.md)

### Example Query

```graphql
query {
  rsm(year: $year) {
    # ... fields
  }
}
```

---

## rsmLeaderboard

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID` | No |  |
| `limit` | `Int` | No |  |

### Returns

`RSMLeaderboard!` → [See RSMLeaderboard](./types/RSMLeaderboard.md)

### Example Query

```graphql
query {
  rsmLeaderboard(tournamentId: $tournamentId, limit: $limit) {
    # ... fields
  }
}
```

---

## ryderCupArticleDetailsCompressed

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `path` | `String!` | Yes |  |

### Returns

`NewsArticleDetailsCompressed!` → [See NewsArticleDetailsCompressed](./types/NewsArticleDetailsCompressed.md)

### Example Query

```graphql
query {
  ryderCupArticleDetailsCompressed(path: $path) {
    # ... fields
  }
}
```

---

## ryderCupBroadcastCoverage

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `eventRegion` | `EventRegion` | No |  |

### Returns

`RyderCupBroadcastCoverage!` → [See RyderCupBroadcastCoverage](./types/RyderCupBroadcastCoverage.md)

### Example Query

```graphql
query {
  ryderCupBroadcastCoverage(eventRegion: $eventRegion) {
    # ... fields
  }
}
```

---

## ryderCupContentFragmentsCompressed

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `TourCode!` | Yes |  |
| `path` | `String` | No |  |
| `limit` | `Int` | No |  |
| `offset` | `Int` | No |  |

### Returns

`ContentFragmentsCompressed!` → [See ContentFragmentsCompressed](./types/ContentFragmentsCompressed.md)

### Example Query

```graphql
query {
  ryderCupContentFragmentsCompressed(tourCode: $tourCode, path: $path, limit: $limit, offset: $offset) {
    # ... fields
  }
}
```

---

## ryderCupContentOptions

### Arguments

None

### Returns

`RyderCupMediaSearchOptions!` → [See RyderCupMediaSearchOptions](./types/RyderCupMediaSearchOptions.md)

### Example Query

```graphql
query {
  ryderCupContentOptions {
    # ... fields
  }
}
```

---

## ryderCupContentPageTabs

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `path` | `String!` | Yes |  |

### Returns

`ContentFragmentTabs!` → [See ContentFragmentTabs](./types/ContentFragmentTabs.md)

### Example Query

```graphql
query {
  ryderCupContentPageTabs(path: $path) {
    # ... fields
  }
}
```

---

## ryderCupMixedMedia

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ascending` | `Boolean!` | Yes |  |
| `type` | `RyderCupContentType` | No |  |
| `team` | `RyderCupTeamType` | No |  |
| `year` | `Int` | No |  |
| `topic` | `String` | No |  |
| `categories` | `[String!]` | No |  |
| `playerIds` | `[String!]` | No |  |
| `articleTags` | `[String!]` | No |  |
| `videoTags` | `[String!]` | No |  |
| `limit` | `Int` | No |  |
| `offset` | `Int` | No |  |
| `currentContentId` | `String` | No |  |

### Returns

`[RyderCupContent!]!` → [See RyderCupContent](./types/RyderCupContent.md)

### Example Query

```graphql
query {
  ryderCupMixedMedia(ascending: $ascending, type: $type, team: $team, year: $year, topic: $topic, categories: $categories, playerIds: $playerIds, articleTags: $articleTags, videoTags: $videoTags, limit: $limit, offset: $offset, currentContentId: $currentContentId) {
    # ... fields
  }
}
```

---

## ryderCupMixedMediaCompressed

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ascending` | `Boolean!` | Yes |  |
| `type` | `RyderCupContentType` | No |  |
| `team` | `RyderCupTeamType` | No |  |
| `year` | `Int` | No |  |
| `topic` | `String` | No |  |
| `categories` | `[String!]` | No |  |
| `playerIds` | `[String!]` | No |  |
| `articleTags` | `[String!]` | No |  |
| `videoTags` | `[String!]` | No |  |
| `limit` | `Int` | No |  |
| `offset` | `Int` | No |  |
| `currentContentId` | `String` | No |  |

### Returns

`RyderCupContentCompressed!` → [See RyderCupContentCompressed](./types/RyderCupContentCompressed.md)

### Example Query

```graphql
query {
  ryderCupMixedMediaCompressed(ascending: $ascending, type: $type, team: $team, year: $year, topic: $topic, categories: $categories, playerIds: $playerIds, articleTags: $articleTags, videoTags: $videoTags, limit: $limit, offset: $offset, currentContentId: $currentContentId) {
    # ... fields
  }
}
```

---

## ryderCupPlayerProfileCompressed

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `playerId` | `String!` | Yes |  |

### Returns

`RyderCupPlayerProfileCompressed!` → [See RyderCupPlayerProfileCompressed](./types/RyderCupPlayerProfileCompressed.md)

### Example Query

```graphql
query {
  ryderCupPlayerProfileCompressed(playerId: $playerId) {
    # ... fields
  }
}
```

---

## ryderCupTeamRankings

**⚠️ DEPRECATED:** use ryderCupTeamRankingsV2

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `year` | `Int` | No |  |
| `eventQuery` | `RyderCupRankingsQueryInput` | No |  |

### Returns

`RyderCupTeamRankings` → [See RyderCupTeamRankings](./types/RyderCupTeamRankings.md)

### Example Query

```graphql
query {
  ryderCupTeamRankings(year: $year, eventQuery: $eventQuery) {
    # ... fields
  }
}
```

---

## ryderCupTeamRankingsCompressed

**⚠️ DEPRECATED:** use ryderCupTeamRankingsCompressedV2

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `year` | `Int` | No |  |
| `eventQuery` | `RyderCupRankingsQueryInput` | No |  |

### Returns

`RyderCupTeamRankingsCompressed` → [See RyderCupTeamRankingsCompressed](./types/RyderCupTeamRankingsCompressed.md)

### Example Query

```graphql
query {
  ryderCupTeamRankingsCompressed(year: $year, eventQuery: $eventQuery) {
    # ... fields
  }
}
```

---

## ryderCupTeamRankingsCompressedV2

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `year` | `Int` | No |  |
| `eventQuery` | `RyderCupRankingsQueryInput` | No |  |

### Returns

`RyderCupTeamRankingsCompressed` → [See RyderCupTeamRankingsCompressed](./types/RyderCupTeamRankingsCompressed.md)

### Example Query

```graphql
query {
  ryderCupTeamRankingsCompressedV2(year: $year, eventQuery: $eventQuery) {
    # ... fields
  }
}
```

---

## ryderCupTeamRankingsV2

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `year` | `Int` | No |  |
| `eventQuery` | `RyderCupRankingsQueryInput` | No |  |

### Returns

`RyderCupRankingsV2` → [See RyderCupRankingsV2](./types/RyderCupRankingsV2.md)

### Example Query

```graphql
query {
  ryderCupTeamRankingsV2(year: $year, eventQuery: $eventQuery) {
    # ... fields
  }
}
```

---

## ryderCupTournament

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `year` | `Int!` | Yes |  |

### Returns

`RyderCupTournament` → [See RyderCupTournament](./types/RyderCupTournament.md)

### Example Query

```graphql
query {
  ryderCupTournament(year: $year) {
    # ... fields
  }
}
```

---

## ryderCupTournaments

### Arguments

None

### Returns

`[RyderCupTournamentOverview!]!` → [See RyderCupTournamentOverview](./types/RyderCupTournamentOverview.md)

### Example Query

```graphql
query {
  ryderCupTournaments {
    # ... fields
  }
}
```

---

## ryderCupVideoById

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `brightcoveId` | `ID!` | Yes |  |

### Returns

`RCVideoPage` → [See RCVideoPage](./types/RCVideoPage.md)

### Example Query

```graphql
query {
  ryderCupVideoById(brightcoveId: $brightcoveId) {
    # ... fields
  }
}
```

---

## scatterData

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `String!` | Yes |  |
| `course` | `Int!` | Yes |  |
| `hole` | `Int!` | Yes |  |

### Returns

`ScatterData!` → [See ScatterData](./types/ScatterData.md)

### Example Query

```graphql
query {
  scatterData(tournamentId: $tournamentId, course: $course, hole: $hole) {
    # ... fields
  }
}
```

---

## scatterDataCompressed

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `String!` | Yes |  |
| `course` | `Int!` | Yes |  |
| `hole` | `Int!` | Yes |  |

### Returns

`ScatterDataCompressed!` → [See ScatterDataCompressed](./types/ScatterDataCompressed.md)

### Example Query

```graphql
query {
  scatterDataCompressed(tournamentId: $tournamentId, course: $course, hole: $hole) {
    # ... fields
  }
}
```

---

## schedule

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `String!` | Yes |  |
| `year` | `String` | No |  |
| `filter` | `TournamentCategory` | No |  |

### Returns

`Schedule!` → [See Schedule](./types/Schedule.md)

### Example Query

```graphql
query {
  schedule(tourCode: $tourCode, year: $year, filter: $filter) {
    # ... fields
  }
}
```

---

## scheduleYears

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `TourCode!` | Yes |  |

### Returns

`ScheduleYears!` → [See ScheduleYears](./types/ScheduleYears.md)

### Example Query

```graphql
query {
  scheduleYears(tourCode: $tourCode) {
    # ... fields
  }
}
```

---

## scorecardCompressedV3

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |
| `playerId` | `ID!` | Yes |  |
| `officialEventData` | `Boolean` | No |  |

### Returns

`ScorecardCompressedV3!` → [See ScorecardCompressedV3](./types/ScorecardCompressedV3.md)

### Example Query

```graphql
query {
  scorecardCompressedV3(tournamentId: $tournamentId, playerId: $playerId, officialEventData: $officialEventData) {
    # ... fields
  }
}
```

---

## scorecardStats

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |
| `playerId` | `ID!` | Yes |  |

### Returns

`PlayerScorecardStats!` → [See PlayerScorecardStats](./types/PlayerScorecardStats.md)

### Example Query

```graphql
query {
  scorecardStats(id: $id, playerId: $playerId) {
    # ... fields
  }
}
```

---

## scorecardStatsComparison

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `String!` | Yes |  |
| `playerIds` | `[String!]!` | Yes |  |
| `round` | `Int` | No |  |
| `category` | `PlayerComparisonCategory!` | Yes |  |

### Returns

`ScorecardStatsComparison` → [See ScorecardStatsComparison](./types/ScorecardStatsComparison.md)

### Example Query

```graphql
query {
  scorecardStatsComparison(tournamentId: $tournamentId, playerIds: $playerIds, round: $round, category: $category) {
    # ... fields
  }
}
```

---

## scorecardStatsV3

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |
| `playerId` | `ID!` | Yes |  |

### Returns

`PlayerScorecardStats!` → [See PlayerScorecardStats](./types/PlayerScorecardStats.md)

### Example Query

```graphql
query {
  scorecardStatsV3(id: $id, playerId: $playerId) {
    # ... fields
  }
}
```

---

## scorecardStatsV3Compressed

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |
| `playerId` | `ID!` | Yes |  |

### Returns

`PlayerScorecardStatsCompressed!` → [See PlayerScorecardStatsCompressed](./types/PlayerScorecardStatsCompressed.md)

### Example Query

```graphql
query {
  scorecardStatsV3Compressed(id: $id, playerId: $playerId) {
    # ... fields
  }
}
```

---

## scorecardV2

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |
| `playerId` | `ID!` | Yes |  |

### Returns

`LeaderboardDrawerV2!` → [See LeaderboardDrawerV2](./types/LeaderboardDrawerV2.md)

### Example Query

```graphql
query {
  scorecardV2(id: $id, playerId: $playerId) {
    # ... fields
  }
}
```

---

## scorecardV3

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |
| `playerId` | `ID!` | Yes |  |
| `officialEventData` | `Boolean` | No |  |

### Returns

`ScorecardV3!` → [See ScorecardV3](./types/ScorecardV3.md)

### Example Query

```graphql
query {
  scorecardV3(tournamentId: $tournamentId, playerId: $playerId, officialEventData: $officialEventData) {
    # ... fields
  }
}
```

---

## searchBarFeatures

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `TourCode` | No |  |

### Returns

`SearchBarFeatures!` → [See SearchBarFeatures](./types/SearchBarFeatures.md)

### Example Query

```graphql
query {
  searchBarFeatures(tourCode: $tourCode) {
    # ... fields
  }
}
```

---

## searchPlayers

**⚠️ DEPRECATED:** No longer supported

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `lastName` | `String` | No |  |

### Returns

`[Player!]!` → [See Player](./types/Player.md)

### Example Query

```graphql
query {
  searchPlayers(lastName: $lastName) {
    # ... fields
  }
}
```

---

## shotDetailsCompressedV3

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |
| `playerId` | `ID!` | Yes |  |
| `round` | `Int!` | Yes |  |
| `includeRadar` | `Boolean` | No |  |

### Returns

`ShotDetailsCompressedV3!` → [See ShotDetailsCompressedV3](./types/ShotDetailsCompressedV3.md)

### Example Query

```graphql
query {
  shotDetailsCompressedV3(tournamentId: $tournamentId, playerId: $playerId, round: $round, includeRadar: $includeRadar) {
    # ... fields
  }
}
```

---

## shotDetailsV3

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |
| `playerId` | `ID!` | Yes |  |
| `round` | `Int!` | Yes |  |
| `includeRadar` | `Boolean` | No |  |

### Returns

`ShotDetails!` → [See ShotDetails](./types/ShotDetails.md)

### Example Query

```graphql
query {
  shotDetailsV3(tournamentId: $tournamentId, playerId: $playerId, round: $round, includeRadar: $includeRadar) {
    # ... fields
  }
}
```

---

## signatureStandings

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `TourCode!` | Yes |  |

### Returns

`SignatureStandings!` → [See SignatureStandings](./types/SignatureStandings.md)

### Example Query

```graphql
query {
  signatureStandings(tourCode: $tourCode) {
    # ... fields
  }
}
```

---

## sponsoredArticles

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `sponsor` | `ArticleSponsor!` | Yes |  |

### Returns

`[NewsArticle!]!` → [See NewsArticle](./types/NewsArticle.md)

### Example Query

```graphql
query {
  sponsoredArticles(sponsor: $sponsor) {
    # ... fields
  }
}
```

---

## sponsoredArticlesV2

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `sponsor` | `ArticleSponsor!` | Yes |  |

### Returns

`SponsoredArticles!` → [See SponsoredArticles](./types/SponsoredArticles.md)

### Example Query

```graphql
query {
  sponsoredArticlesV2(sponsor: $sponsor) {
    # ... fields
  }
}
```

---

## sponsorships

**⚠️ DEPRECATED:** use REST API

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `playerId` | `ID!` | Yes |  |

### Returns

`PlayerSponsors!` → [See PlayerSponsors](./types/PlayerSponsors.md)

### Example Query

```graphql
query {
  sponsorships(playerId: $playerId) {
    # ... fields
  }
}
```

---

## statDetails

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `TourCode!` | Yes |  |
| `statId` | `String!` | Yes |  |
| `year` | `Int` | No |  |
| `eventQuery` | `StatDetailEventQuery` | No |  |

### Returns

`StatDetails!` → [See StatDetails](./types/StatDetails.md)

### Example Query

```graphql
query {
  statDetails(tourCode: $tourCode, statId: $statId, year: $year, eventQuery: $eventQuery) {
    # ... fields
  }
}
```

---

## statLeaders

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `TourCode!` | Yes |  |
| `category` | `StatCategory!` | Yes |  |
| `year` | `Int` | No |  |

### Returns

`StatLeaderCategory!` → [See StatLeaderCategory](./types/StatLeaderCategory.md)

### Example Query

```graphql
query {
  statLeaders(tourCode: $tourCode, category: $category, year: $year) {
    # ... fields
  }
}
```

---

## statOverview

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `TourCode!` | Yes |  |
| `year` | `Int` | No |  |

### Returns

`OverviewStats!` → [See OverviewStats](./types/OverviewStats.md)

### Example Query

```graphql
query {
  statOverview(tourCode: $tourCode, year: $year) {
    # ... fields
  }
}
```

---

## statsLeadersMobile

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `TourCode!` | Yes |  |
| `year` | `Int` | No |  |

### Returns

`MobileStatLeaders!` → [See MobileStatLeaders](./types/MobileStatLeaders.md)

### Example Query

```graphql
query {
  statsLeadersMobile(tourCode: $tourCode, year: $year) {
    # ... fields
  }
}
```

---

## teamStrokePlayLeaderboard

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`TSPLeaderboard!` → [See TSPLeaderboard](./types/TSPLeaderboard.md)

### Example Query

```graphql
query {
  teamStrokePlayLeaderboard(id: $id) {
    # ... fields
  }
}
```

---

## teamStrokePlayLeaderboardCompressed

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`LeaderboardCompressed!` → [See LeaderboardCompressed](./types/LeaderboardCompressed.md)

### Example Query

```graphql
query {
  teamStrokePlayLeaderboardCompressed(id: $id) {
    # ... fields
  }
}
```

---

## teamStrokePlayScorecard

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |
| `roundNum` | `Int!` | Yes |  |
| `teamId` | `ID!` | Yes |  |

### Returns

`TSPScorecard!` → [See TSPScorecard](./types/TSPScorecard.md)

### Example Query

```graphql
query {
  teamStrokePlayScorecard(tournamentId: $tournamentId, roundNum: $roundNum, teamId: $teamId) {
    # ... fields
  }
}
```

---

## teamStrokePlayScorecardRounds

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |
| `teamId` | `ID!` | Yes |  |

### Returns

`TSPScorecardRounds!` → [See TSPScorecardRounds](./types/TSPScorecardRounds.md)

### Example Query

```graphql
query {
  teamStrokePlayScorecardRounds(tournamentId: $tournamentId, teamId: $teamId) {
    # ... fields
  }
}
```

---

## teamStrokePlayTeeTimes

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |

### Returns

`TSPTeeTimes!` → [See TSPTeeTimes](./types/TSPTeeTimes.md)

### Example Query

```graphql
query {
  teamStrokePlayTeeTimes(tournamentId: $tournamentId) {
    # ... fields
  }
}
```

---

## teamStrokePlayTeeTimesCompressed

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |

### Returns

`TeeTimesCompressed!` → [See TeeTimesCompressed](./types/TeeTimesCompressed.md)

### Example Query

```graphql
query {
  teamStrokePlayTeeTimesCompressed(tournamentId: $tournamentId) {
    # ... fields
  }
}
```

---

## teeTimes

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`TeeTimes!` → [See TeeTimes](./types/TeeTimes.md)

### Example Query

```graphql
query {
  teeTimes(id: $id) {
    # ... fields
  }
}
```

---

## teeTimesCompressed

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`TeeTimesCompressed!` → [See TeeTimesCompressed](./types/TeeTimesCompressed.md)

### Example Query

```graphql
query {
  teeTimesCompressed(id: $id) {
    # ... fields
  }
}
```

---

## teeTimesCompressedV2

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`TeeTimesCompressed!` → [See TeeTimesCompressed](./types/TeeTimesCompressed.md)

### Example Query

```graphql
query {
  teeTimesCompressedV2(id: $id) {
    # ... fields
  }
}
```

---

## teeTimesV2

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`TeeTimesV2!` → [See TeeTimesV2](./types/TeeTimesV2.md)

### Example Query

```graphql
query {
  teeTimesV2(id: $id) {
    # ... fields
  }
}
```

---

## tglMatch

  Returns full details for matches based on supplied matchIds

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `matchId` | `ID!` | Yes |  |

### Returns

`TGLMatch` → [See TGLMatch](./types/TGLMatch.md)

### Example Query

```graphql
query {
  tglMatch(matchId: $matchId) {
    # ... fields
  }
}
```

---

## tglMatches

  return a season from TGL based on supplied year, if year is ommitted current year returned, used by AEM

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `matchIds` | `[ID!]!` | Yes |  |

### Returns

`[TGLMatch!]!` → [See TGLMatch](./types/TGLMatch.md)

### Example Query

```graphql
query {
  tglMatches(matchIds: $matchIds) {
    # ... fields
  }
}
```

---

## tglSchedule

 ## TGL queries

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `year` | `Int` | No |  |
| `offset` | `Int` | No |  |
| `limit` | `Int` | No |  |

### Returns

`TGLSchedule!` → [See TGLSchedule](./types/TGLSchedule.md)

### Example Query

```graphql
query {
  tglSchedule(year: $year, offset: $offset, limit: $limit) {
    # ... fields
  }
}
```

---

## tourCup

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |
| `type` | `TourCupType` | No |  |

### Returns

`TourCupRankingEvent!` → [See TourCupRankingEvent](./types/TourCupRankingEvent.md)

### Example Query

```graphql
query {
  tourCup(id: $id, type: $type) {
    # ... fields
  }
}
```

---

## tourCupCombined

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `TourCode!` | Yes |  |
| `id` | `String` | No |  |
| `year` | `Int` | No |  |
| `eventQuery` | `StatDetailEventQuery` | No |  |

### Returns

`TourCupCombined!` → [See TourCupCombined](./types/TourCupCombined.md)

### Example Query

```graphql
query {
  tourCupCombined(tourCode: $tourCode, id: $id, year: $year, eventQuery: $eventQuery) {
    # ... fields
  }
}
```

---

## tourCupSplit

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `TourCode!` | Yes |  |
| `id` | `String` | No |  |
| `year` | `Int` | No |  |
| `eventQuery` | `StatDetailEventQuery` | No |  |

### Returns

`TourCupSplit` → [See TourCupSplit](./types/TourCupSplit.md)

### Example Query

```graphql
query {
  tourCupSplit(tourCode: $tourCode, id: $id, year: $year, eventQuery: $eventQuery) {
    # ... fields
  }
}
```

---

## tourCups

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tour` | `TourCode!` | Yes |  |
| `year` | `Int!` | Yes |  |

### Returns

`[TourCupRankingEvent!]!` → [See TourCupRankingEvent](./types/TourCupRankingEvent.md)

### Example Query

```graphql
query {
  tourCups(tour: $tour, year: $year) {
    # ... fields
  }
}
```

---

## tourcastTable

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |

### Returns

`TourcastTable!` → [See TourcastTable](./types/TourcastTable.md)

### Example Query

```graphql
query {
  tourcastTable(tournamentId: $tournamentId) {
    # ... fields
  }
}
```

---

## tourcastVideos

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |
| `playerId` | `ID!` | Yes |  |
| `round` | `Int!` | Yes |  |
| `hole` | `Int` | No |  |
| `shot` | `Int` | No |  |

### Returns

`[Video!]!` → [See Video](./types/Video.md)

### Example Query

```graphql
query {
  tourcastVideos(tournamentId: $tournamentId, playerId: $playerId, round: $round, hole: $hole, shot: $shot) {
    # ... fields
  }
}
```

---

## tournamentGroupLocations

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |
| `round` | `Int!` | Yes |  |

### Returns

`TournamentGroupLocation!` → [See TournamentGroupLocation](./types/TournamentGroupLocation.md)

### Example Query

```graphql
query {
  tournamentGroupLocations(tournamentId: $tournamentId, round: $round) {
    # ... fields
  }
}
```

---

## tournamentHistory

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `String!` | Yes |  |

### Returns

`TournamentHistory` → [See TournamentHistory](./types/TournamentHistory.md)

### Example Query

```graphql
query {
  tournamentHistory(tournamentId: $tournamentId) {
    # ... fields
  }
}
```

---

## tournamentOddsCompressedV2

**⚠️ DEPRECATED:** DOES NOT WORK USE oddsWin / REST APIs

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |
| `provider` | `OddsProvider` | No |  |
| `oddsFormat` | `OddsFormat` | No |  |

### Returns

`TournamentOddsCompressedV2!` → [See TournamentOddsCompressedV2](./types/TournamentOddsCompressedV2.md)

### Example Query

```graphql
query {
  tournamentOddsCompressedV2(tournamentId: $tournamentId, provider: $provider, oddsFormat: $oddsFormat) {
    # ... fields
  }
}
```

---

## tournamentOddsToWin

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |

### Returns

`TournamentOddsToWin!` → [See TournamentOddsToWin](./types/TournamentOddsToWin.md)

### Example Query

```graphql
query {
  tournamentOddsToWin(tournamentId: $tournamentId) {
    # ... fields
  }
}
```

---

## tournamentOddsV2

**⚠️ DEPRECATED:** DOES NOT WORK USE oddsToWin / REST APIs

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |
| `provider` | `OddsProvider` | No |  |
| `oddsFormat` | `OddsFormat` | No |  |

### Returns

`TournamentOddsV2!` → [See TournamentOddsV2](./types/TournamentOddsV2.md)

### Example Query

```graphql
query {
  tournamentOddsV2(tournamentId: $tournamentId, provider: $provider, oddsFormat: $oddsFormat) {
    # ... fields
  }
}
```

---

## tournamentOverview

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |

### Returns

`TournamentOverview!` → [See TournamentOverview](./types/TournamentOverview.md)

### Example Query

```graphql
query {
  tournamentOverview(tournamentId: $tournamentId) {
    # ... fields
  }
}
```

---

## tournamentPastResults

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |
| `year` | `Int` | No |  |

### Returns

`HistoricalLeaderboard!` → [See HistoricalLeaderboard](./types/HistoricalLeaderboard.md)

### Example Query

```graphql
query {
  tournamentPastResults(id: $id, year: $year) {
    # ... fields
  }
}
```

---

## tournamentRecap

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `String!` | Yes |  |
| `limit` | `Int` | No |  |
| `offset` | `Int` | No |  |

### Returns

`TournamentRecap!` → [See TournamentRecap](./types/TournamentRecap.md)

### Example Query

```graphql
query {
  tournamentRecap(tournamentId: $tournamentId, limit: $limit, offset: $offset) {
    # ... fields
  }
}
```

---

## tournaments

  Get tournament information for the given tournament IDs

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ids` | `[ID!]` | No |  |

### Returns

`[Tournament!]!` → [See Tournament](./types/Tournament.md)

### Example Query

```graphql
query {
  tournaments(ids: $ids) {
    # ... fields
  }
}
```

---

## tspPlayoffShotDetails

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |
| `includeRadar` | `Boolean` | No |  |

### Returns

`TeamShotDetails!` → [See TeamShotDetails](./types/TeamShotDetails.md)

### Example Query

```graphql
query {
  tspPlayoffShotDetails(tournamentId: $tournamentId, includeRadar: $includeRadar) {
    # ... fields
  }
}
```

---

## tspPlayoffShotDetailsCompressed

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |
| `includeRadar` | `Boolean` | No |  |

### Returns

`TeamShotDetailsCompressed!` → [See TeamShotDetailsCompressed](./types/TeamShotDetailsCompressed.md)

### Example Query

```graphql
query {
  tspPlayoffShotDetailsCompressed(tournamentId: $tournamentId, includeRadar: $includeRadar) {
    # ... fields
  }
}
```

---

## universityRankings

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `year` | `Int` | No |  |
| `week` | `Int` | No |  |
| `tourCode` | `TourCode` | No |  |

### Returns

`UniversityRankings!` → [See UniversityRankings](./types/UniversityRankings.md)

### Example Query

```graphql
query {
  universityRankings(year: $year, week: $week, tourCode: $tourCode) {
    # ... fields
  }
}
```

---

## universityTotalPoints

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `season` | `Int` | No |  |
| `week` | `Int` | No |  |

### Returns

`UniversityTotalPoints!` → [See UniversityTotalPoints](./types/UniversityTotalPoints.md)

### Example Query

```graphql
query {
  universityTotalPoints(season: $season, week: $week) {
    # ... fields
  }
}
```

---

## upcomingNetworks

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentIds` | `[ID!]!` | Yes |  |
| `tourCode` | `TourCode` | No |  |

### Returns

`UpcomingBroadcastNetworks!` → [See UpcomingBroadcastNetworks](./types/UpcomingBroadcastNetworks.md)

### Example Query

```graphql
query {
  upcomingNetworks(tournamentIds: $tournamentIds, tourCode: $tourCode) {
    # ... fields
  }
}
```

---

## upcomingSchedule

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `String!` | Yes |  |
| `year` | `String` | No |  |
| `filter` | `TournamentCategory` | No |  |

### Returns

`ScheduleUpcoming!` → [See ScheduleUpcoming](./types/ScheduleUpcoming.md)

### Example Query

```graphql
query {
  upcomingSchedule(tourCode: $tourCode, year: $year, filter: $filter) {
    # ... fields
  }
}
```

---

## videoById

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `brightcoveId` | `ID!` | Yes |  |
| `tourcast` | `Boolean!` | Yes |  |

### Returns

`Video` → [See Video](./types/Video.md)

### Example Query

```graphql
query {
  videoById(brightcoveId: $brightcoveId, tourcast: $tourcast) {
    # ... fields
  }
}
```

---

## videoFranchises

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `TourCode` | No |  |

### Returns

`TourCategories` → [See TourCategories](./types/TourCategories.md)

### Example Query

```graphql
query {
  videoFranchises(tourCode: $tourCode) {
    # ... fields
  }
}
```

---

## videoHero

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `TourCode!` | Yes |  |
| `path` | `String` | No |  |

### Returns

`VideoHero!` → [See VideoHero](./types/VideoHero.md)

### Example Query

```graphql
query {
  videoHero(tourCode: $tourCode, path: $path) {
    # ... fields
  }
}
```

---

## videoLandingPage

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `TourCode!` | Yes |  |

### Returns

`WatchLanding` → [See WatchLanding](./types/WatchLanding.md)

### Example Query

```graphql
query {
  videoLandingPage(tourCode: $tourCode) {
    # ... fields
  }
}
```

---

## videoNavigation

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `TourCode!` | Yes |  |

### Returns

`VideoNavigation` → [See VideoNavigation](./types/VideoNavigation.md)

### Example Query

```graphql
query {
  videoNavigation(tourCode: $tourCode) {
    # ... fields
  }
}
```

---

## videoRecommendations

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `brightcoveId` | `ID` | No |  |
| `tournamentId` | `String` | No |  |
| `playerId` | `String` | No |  |
| `franchise` | `String` | No |  |
| `tour` | `String` | No |  |
| `tourCode` | `TourCode` | No |  |
| `season` | `String` | No |  |
| `limit` | `Int` | No |  |
| `offset` | `Int` | No |  |
| `language` | `VideoLanguage` | No |  |

### Returns

`[Video!]!` → [See Video](./types/Video.md)

### Example Query

```graphql
query {
  videoRecommendations(brightcoveId: $brightcoveId, tournamentId: $tournamentId, playerId: $playerId, franchise: $franchise, tour: $tour, tourCode: $tourCode, season: $season, limit: $limit, offset: $offset, language: $language) {
    # ... fields
  }
}
```

---

## videos

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `String` | No |  |
| `playerId` | `String` | No |  |
| `playerIds` | `[String!]` | No |  |
| `rating` | `Int` | No |  |
| `category` | `String` | No |  |
| `franchise` | `String` | No |  |
| `franchises` | `[String!]` | No |  |
| `tour` | `String` | No |  |
| `tourCode` | `TourCode` | No |  |
| `season` | `String` | No |  |
| `limit` | `Int` | No |  |
| `offset` | `Int` | No |  |
| `holeNumber` | `String` | No |  |
| `language` | `VideoLanguage` | No |  |

### Returns

`[Video!]!` → [See Video](./types/Video.md)

### Example Query

```graphql
query {
  videos(tournamentId: $tournamentId, playerId: $playerId, playerIds: $playerIds, rating: $rating, category: $category, franchise: $franchise, franchises: $franchises, tour: $tour, tourCode: $tourCode, season: $season, limit: $limit, offset: $offset, holeNumber: $holeNumber, language: $language) {
    # ... fields
  }
}
```

---

## weather

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |

### Returns

`WeatherSummary!` → [See WeatherSummary](./types/WeatherSummary.md)

### Example Query

```graphql
query {
  weather(tournamentId: $tournamentId) {
    # ... fields
  }
}
```

---

## yourTour

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `TourCode!` | Yes |  |

### Returns

`YourTourStory!` → [See YourTourStory](./types/YourTourStory.md)

### Example Query

```graphql
query {
  yourTour(tourCode: $tourCode) {
    # ... fields
  }
}
```

---

## yourTourNews

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `TourCode!` | Yes |  |
| `limit` | `Int` | No |  |
| `offset` | `Int` | No |  |

### Returns

`[YourTourNews!]!` → [See YourTourNews](./types/YourTourNews.md)

### Example Query

```graphql
query {
  yourTourNews(tourCode: $tourCode, limit: $limit, offset: $offset) {
    # ... fields
  }
}
```

---


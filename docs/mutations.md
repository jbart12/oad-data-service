# PGA Tour GraphQL API - Complete Mutations Reference

**Total Mutations: 64**

---

## Table of Contents

- [addFavoriteTour](#addfavoritetour)
- [addFavorites](#addfavorites)
- [addNotificationTags](#addnotificationtags)
- [deleteAccount](#deleteaccount)
- [deleteFavorites](#deletefavorites)
- [deleteNotificationTags](#deletenotificationtags)
- [unsubscribe](#unsubscribe)
- [updateBubble](#updatebubble)
- [updateBubbleWatch](#updatebubblewatch)
- [updateCourseStats](#updatecoursestats)
- [updateCoverage](#updatecoverage)
- [updateCupOverviewLeaderboard](#updatecupoverviewleaderboard)
- [updateCupRoundLeaderboard](#updatecuproundleaderboard)
- [updateCupRoundLeaderboardCompressed](#updatecuproundleaderboardcompressed)
- [updateCupScorecard](#updatecupscorecard)
- [updateCurrentLeadersCompressed](#updatecurrentleaderscompressed)
- [updateGroupLocations](#updategrouplocations)
- [updateGroupLocationsEnhanced](#updategrouplocationsenhanced)
- [updateHoleDetails](#updateholedetails)
- [updateLeaderboardCompressedV2](#updateleaderboardcompressedv2)
- [updateLeaderboardCompressedV3](#updateleaderboardcompressedv3)
- [updateLeaderboardStrokes](#updateleaderboardstrokes)
- [updateLeaderboardStrokesCompressed](#updateleaderboardstrokescompressed)
- [updateLeaderboardV2](#updateleaderboardv2)
- [updateMatchOutcomeIq](#updatematchoutcomeiq)
- [updateMatchPlayLeaderboard](#updatematchplayleaderboard)
- [updateMatchPlayLeaderboardCompressed](#updatematchplayleaderboardcompressed)
- [updateMatchPlayPlayoffScorecard](#updatematchplayplayoffscorecard)
- [updateMatchPlayScorecard](#updatematchplayscorecard)
- [updateMatchPlayTeeTimes](#updatematchplayteetimes)
- [updateMatchPlayTeeTimesCompressed](#updatematchplayteetimescompressed)
- [updateOddsToWinMarket](#updateoddstowinmarket)
- [updateOddsToWinMarketCompressed](#updateoddstowinmarketcompressed)
- [updatePlayerHub](#updateplayerhub)
- [updatePlayerTournamentStatus](#updateplayertournamentstatus)
- [updatePlayoffScorecard](#updateplayoffscorecard)
- [updatePlayoffScorecardV2](#updateplayoffscorecardv2)
- [updatePlayoffScorecardV3](#updateplayoffscorecardv3)
- [updatePlayoffShotDetails](#updateplayoffshotdetails)
- [updatePlayoffShotDetailsCompressed](#updateplayoffshotdetailscompressed)
- [updateScorecardCompressedV3](#updatescorecardcompressedv3)
- [updateScorecardStats](#updatescorecardstats)
- [updateScorecardStatsCompressedV3](#updatescorecardstatscompressedv3)
- [updateScorecardV2](#updatescorecardv2)
- [updateShotCommentary](#updateshotcommentary)
- [updateShotDetailsCompressedV3](#updateshotdetailscompressedv3)
- [updateTGLMatch](#updatetglmatch)
- [updateTSPPlayoffShotDetails](#updatetspplayoffshotdetails)
- [updateTSPPlayoffShotDetailsCompressed](#updatetspplayoffshotdetailscompressed)
- [updateTeamPlayLeaderboard](#updateteamplayleaderboard)
- [updateTeamPlayLeaderboardCompressed](#updateteamplayleaderboardcompressed)
- [updateTeamPlayScorecard](#updateteamplayscorecard)
- [updateTeamPlayScorecardRounds](#updateteamplayscorecardrounds)
- [updateTeamStrokePlayTeeTimes](#updateteamstrokeplayteetimes)
- [updateTeamStrokePlayTeeTimesCompressed](#updateteamstrokeplayteetimescompressed)
- [updateTeeTimes](#updateteetimes)
- [updateTeeTimesCompressed](#updateteetimescompressed)
- [updateTeeTimesCompressedV2](#updateteetimescompressedv2)
- [updateTeeTimesV2](#updateteetimesv2)
- [updateTourCup](#updatetourcup)
- [updateTourcastTable](#updatetourcasttable)
- [updateTournament](#updatetournament)
- [updateTournamentGroupLocations](#updatetournamentgrouplocations)
- [updateUpcomingSchedule](#updateupcomingschedule)

---

## addFavoriteTour

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `TourCode!` | Yes |  |

### Returns

`FavoriteTourResponse!`

---

## addFavorites

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `favorites` | `[FavoritePlayerInput!]!` | Yes |  |

### Returns

`[FavoritePlayer!]!`

---

## addNotificationTags

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `notificationTags` | `[NotificationTagInput!]!` | Yes |  |

### Returns

`NotificationTagResponse!`

---

## deleteAccount

### Returns

`DeleteAccountResponse!`

---

## deleteFavorites

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `favorites` | `[FavoritePlayerInput!]!` | Yes |  |

### Returns

`[FavoritePlayer!]!`

---

## deleteNotificationTags

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `notificationTags` | `[NotificationTagInput!]!` | Yes |  |

### Returns

`NotificationTagResponse!`

---

## unsubscribe

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `subscriptionIds` | `[String]!` | Yes |  |
| `email` | `String!` | Yes |  |

### Returns

`UnsubscribeResponse!`

---

## updateBubble

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `bubbleId` | `ID!` | Yes |  |

### Returns

`BubbleWatch`

---

## updateBubbleWatch

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `TourCode!` | Yes |  |

### Returns

`TourCupRankingEvent`

---

## updateCourseStats

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |

### Returns

`TournamentHoleStats`

---

## updateCoverage

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |

### Returns

`BroadcastCoverage`

---

## updateCupOverviewLeaderboard

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`CupTournamentStatus`

---

## updateCupRoundLeaderboard

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `String!` | Yes |  |
| `round` | `Int` | No |  |

### Returns

`CupTournamentLeaderboard`

---

## updateCupRoundLeaderboardCompressed

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `String!` | Yes |  |
| `round` | `Int` | No |  |

### Returns

`CupTournamentLeaderboardCompressed`

---

## updateCupScorecard

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |
| `round` | `Int!` | Yes |  |
| `matchId` | `Int!` | Yes |  |

### Returns

`CupScorecard`

---

## updateCurrentLeadersCompressed

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |

### Returns

`CurrentLeadersCompressed`

---

## updateGroupLocations

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |
| `round` | `Int!` | Yes |  |
| `courseId` | `String!` | Yes |  |

### Returns

`GroupLocationCourse`

---

## updateGroupLocationsEnhanced

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |
| `round` | `Int!` | Yes |  |
| `courseId` | `String!` | Yes |  |

### Returns

`GroupLocationCourse`

---

## updateHoleDetails

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |
| `courseId` | `ID!` | Yes |  |
| `hole` | `Int!` | Yes |  |

### Returns

`HoleDetail`

---

## updateLeaderboardCompressedV2

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`LeaderboardCompressedV2`

---

## updateLeaderboardCompressedV3

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |
| `odds` | `OddsUpdateInput` | No |  |

### Returns

`LeaderboardUpdateCompressedV3`

---

## updateLeaderboardStrokes

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`LeaderboardStrokes`

---

## updateLeaderboardStrokesCompressed

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`LeaderboardStrokesCompressed`

---

## updateLeaderboardV2

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`LeaderboardV2`

---

## updateMatchOutcomeIq

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |
| `matchId` | `Int!` | Yes |  |
| `roundNumber` | `Int` | No |  |

### Returns

`RyderCupMatchOutcomeIQ`

---

## updateMatchPlayLeaderboard

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`MPLeaderboard`

---

## updateMatchPlayLeaderboardCompressed

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`LeaderboardCompressed`

---

## updateMatchPlayPlayoffScorecard

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`MPPlayoffScorecard`

---

## updateMatchPlayScorecard

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`MPScorecard`

---

## updateMatchPlayTeeTimes

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`MPTeeTimes!`

---

## updateMatchPlayTeeTimesCompressed

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`TeeTimesCompressed`

---

## updateOddsToWinMarket

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `oddsToWinId` | `ID!` | Yes |  |

### Returns

`OddsToWinMarket`

---

## updateOddsToWinMarketCompressed

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `oddsToWinId` | `ID!` | Yes |  |

### Returns

`OddsToWinMarketCompressed`

---

## updatePlayerHub

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`PlayerHubPlayerCompressed`

---

## updatePlayerTournamentStatus

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `playerId` | `ID!` | Yes |  |
| `tournamentId` | `String!` | Yes |  |

### Returns

`PlayerTournamentStatus`

---

## updatePlayoffScorecard

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`PlayoffScorecard`

---

## updatePlayoffScorecardV2

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`[PlayoffScorecard!]!`

---

## updatePlayoffScorecardV3

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |

### Returns

`TournamentPlayoffScorecards!`

---

## updatePlayoffShotDetails

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |

### Returns

`GroupShotDetails!`

---

## updatePlayoffShotDetailsCompressed

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |

### Returns

`GroupShotDetailsCompressed!`

---

## updateScorecardCompressedV3

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |
| `rounds` | `[Int!]` | No |  |

### Returns

`ScorecardUpdateCompressedV3`

---

## updateScorecardStats

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |
| `playerId` | `String!` | Yes |  |

### Returns

`PlayerScorecardStats`

---

## updateScorecardStatsCompressedV3

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |
| `playerId` | `String!` | Yes |  |
| `rounds` | `[Int!]!` | Yes |  |

### Returns

`PlayerScorecardStatsCompressed`

---

## updateScorecardV2

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`LeaderboardDrawerV2`

---

## updateShotCommentary

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `String!` | Yes |  |
| `playerId` | `String!` | Yes |  |
| `round` | `Int!` | Yes |  |
| `commentary` | `[ShotCommentaryItemInput!]!` | Yes |  |

### Returns

`ShotCommentary`

---

## updateShotDetailsCompressedV3

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `String!` | Yes |  |
| `playerId` | `String!` | Yes |  |
| `round` | `Int!` | Yes |  |
| `holes` | `[Int!]!` | Yes |  |
| `tourcast` | `Boolean!` | Yes |  |
| `isUs` | `Boolean!` | Yes |  |

### Returns

`ShotDetailsCompressedV3`

---

## updateTGLMatch

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `matchID` | `ID!` | Yes |  |

### Returns

`TGLMatch`

---

## updateTSPPlayoffShotDetails

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |

### Returns

`TeamShotDetails!`

---

## updateTSPPlayoffShotDetailsCompressed

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |

### Returns

`TeamShotDetailsCompressed!`

---

## updateTeamPlayLeaderboard

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |
| `provider` | `String!` | Yes |  |

### Returns

`TSPLeaderboard`

---

## updateTeamPlayLeaderboardCompressed

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |
| `provider` | `String!` | Yes |  |

### Returns

`LeaderboardCompressed`

---

## updateTeamPlayScorecard

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`TSPScorecard`

---

## updateTeamPlayScorecardRounds

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`TSPScorecardRounds`

---

## updateTeamStrokePlayTeeTimes

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`TSPTeeTimes`

---

## updateTeamStrokePlayTeeTimesCompressed

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`TeeTimesCompressed`

---

## updateTeeTimes

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`TeeTimes`

---

## updateTeeTimesCompressed

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`TeeTimesCompressed`

---

## updateTeeTimesCompressedV2

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`TeeTimesCompressed`

---

## updateTeeTimesV2

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`TeeTimesV2`

---

## updateTourCup

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |
| `type` | `TourCupType` | No |  |

### Returns

`TourCupRankingEvent`

---

## updateTourcastTable

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |

### Returns

`TourcastTable`

---

## updateTournament

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `ID!` | Yes |  |

### Returns

`Tournament`

---

## updateTournamentGroupLocations

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tournamentId` | `ID!` | Yes |  |
| `round` | `Int!` | Yes |  |

### Returns

`TournamentGroupLocation`

---

## updateUpcomingSchedule

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tourCode` | `String!` | Yes |  |
| `year` | `String` | No |  |

### Returns

`ScheduleUpcoming`

---


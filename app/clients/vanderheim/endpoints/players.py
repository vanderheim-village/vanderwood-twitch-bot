from typing import Any, Dict, Optional

from app.clients.vanderheim.base_client import BaseAPIClient


class PlayersAPI:
    def __init__(self, client: BaseAPIClient):
        self.client = client

    async def _fetch_players_page(
        self, page: Optional[int] = None, page_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of players.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/players/"
        return await self.client._get(url, params=params)

    async def fetch_all_players(self) -> Dict[str, Any]:
        """
        Fetches all players using the fetch_players_page method.
        """
        all_players = []
        page = 1
        while True:
            response = await self._fetch_players_page(page=page)
            players = response["results"]
            all_players.extend(players)
            if not response["next"]:
                break
            page += 1
        return {"results": all_players}

    async def fetch_player(self, player_id: str) -> Dict[str, Any]:
        """
        Fetches a single player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/"
        return await self.client._get(url)

    async def create_player(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new player.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/"
        return await self.client._post(url, data)

    async def update_player(self, player_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates an existing player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/"
        return await self.client._put(url, data)

    async def partial_update_player(self, player_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Partially updates an existing player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/"
        return await self.client._patch(url, data)

    async def delete_player(self, player_id: str) -> None:
        """
        Deletes an existing player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/"
        return await self.client._delete(url)

    async def _fetch_player_checkins_page(
        self, player_id: str, page: Optional[int] = None, page_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of check-ins for a player.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/checkins/"
        return await self.client._get(url, params=params)

    async def fetch_player_checkins(self, player_id: str) -> Dict[str, Any]:
        """
        Fetches all check-ins for a player using the fetch_player_checkins_page method.
        """
        all_checkins = []
        page = 1
        while True:
            response = await self._fetch_player_checkins_page(player_id, page=page)
            checkins = response["results"]
            all_checkins.extend(checkins)
            if not response["next"]:
                break
            page += 1
        return {"results": all_checkins}

    async def fetch_player_checkin(self, player_id: str, checkin_id: str) -> Dict[str, Any]:
        """
        Fetches a single check-in for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/checkins/{checkin_id}/"
        return await self.client._get(url)

    async def create_player_checkin(self, player_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new check-in for a player.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/checkins/"
        return await self.client._post(url, data)

    async def update_player_checkin(
        self, player_id: str, checkin_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Updates an existing check-in for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/checkins/{checkin_id}/"
        return await self.client._put(url, data)

    async def partial_update_player_checkin(
        self, player_id: str, checkin_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Partially updates an existing check-in for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/checkins/{checkin_id}/"
        return await self.client._patch(url, data)

    async def delete_player_checkin(self, player_id: str, checkin_id: str) -> None:
        """
        Deletes an existing check-in for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/checkins/{checkin_id}/"
        return await self.client._delete(url)

    async def _fetch_player_clan_spoils_claims_page(
        self, player_id: str, page: Optional[int] = None, page_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of clan spoils claims for a player.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/clan-spoils-claims/"
        return await self.client._get(url, params=params)

    async def fetch_player_clan_spoils_claims(self, player_id: str) -> Dict[str, Any]:
        """
        Fetches all clan spoils claims for a player using the fetch_player_clan_spoils_claims_page method.
        """
        all_clan_spoils_claims = []
        page = 1
        while True:
            response = await self._fetch_player_clan_spoils_claims_page(player_id, page=page)
            clan_spoils_claims = response["results"]
            all_clan_spoils_claims.extend(clan_spoils_claims)
            if not response["next"]:
                break
            page += 1
        return {"results": all_clan_spoils_claims}

    async def fetch_player_clan_spoils_claim(
        self, player_id: str, clan_spoils_claim_id: str
    ) -> Dict[str, Any]:
        """
        Fetches a single clan spoils claim for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/clan-spoils-claims/{clan_spoils_claim_id}/"
        return await self.client._get(url)

    async def create_player_clan_spoils_claim(
        self, player_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Creates a new clan spoils claim for a player.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/clan-spoils-claims/"
        return await self.client._post(url, data)

    async def update_player_clan_spoils_claim(
        self, player_id: str, clan_spoils_claim_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Updates an existing clan spoils claim for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/clan-spoils-claims/{clan_spoils_claim_id}/"
        return await self.client._put(url, data)

    async def partial_update_player_clan_spoils_claim(
        self, player_id: str, clan_spoils_claim_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Partially updates an existing clan spoils claim for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/clan-spoils-claims/{clan_spoils_claim_id}/"
        return await self.client._patch(url, data)

    async def delete_player_clan_spoils_claim(
        self, player_id: str, clan_spoils_claim_id: str
    ) -> None:
        """
        Deletes an existing clan spoils claim for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/clan-spoils-claims/{clan_spoils_claim_id}/"
        return await self.client._delete(url)

    async def _fetch_player_gifted_subscriptions_page(
        self, player_id: str, page: Optional[int] = None, page_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of gifted subscriptions for a player.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/gifted-subscriptions/"
        return await self.client._get(url, params=params)

    async def fetch_player_gifted_subscriptions(self, player_id: str) -> Dict[str, Any]:
        """
        Fetches all gifted subscriptions for a player using the fetch_player_gifted_subscriptions_page method.
        """
        all_gifted_subscriptions = []
        page = 1
        while True:
            response = await self._fetch_player_gifted_subscriptions_page(player_id, page=page)
            gifted_subscriptions = response["results"]
            all_gifted_subscriptions.extend(gifted_subscriptions)
            if not response["next"]:
                break
            page += 1
        return {"results": all_gifted_subscriptions}

    async def fetch_player_gifted_subscription(
        self, player_id: str, gifted_subscription_id: str
    ) -> Dict[str, Any]:
        """
        Fetches a single gifted subscription for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/gifted-subscriptions/{gifted_subscription_id}/"
        return await self.client._get(url)

    async def create_player_gifted_subscription(
        self, player_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Creates a new gifted subscription for a player.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/gifted-subscriptions/"
        return await self.client._post(url, data)

    async def update_player_gifted_subscription(
        self, player_id: str, gifted_subscription_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Updates an existing gifted subscription for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/gifted-subscriptions/{gifted_subscription_id}/"
        return await self.client._put(url, data)

    async def partial_update_player_gifted_subscription(
        self, player_id: str, gifted_subscription_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Partially updates an existing gifted subscription for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/gifted-subscriptions/{gifted_subscription_id}/"
        return await self.client._patch(url, data)

    async def delete_player_gifted_subscription(
        self, player_id: str, gifted_subscription_id: str
    ) -> None:
        """
        Deletes an existing gifted subscription for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/gifted-subscriptions/{gifted_subscription_id}/"
        return await self.client._delete(url)

    async def _fetch_player_player_watch_times_page(
        self, player_id: str, page: Optional[int] = None, page_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of watch times for a player.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/player-watch-times/"
        return await self.client._get(url, params=params)

    async def fetch_player_player_watch_times(self, player_id: str) -> Dict[str, Any]:
        """
        Fetches all watch times for a player using the fetch_player_player_watch_times_page method.
        """
        all_player_watch_times = []
        page = 1
        while True:
            response = await self._fetch_player_player_watch_times_page(player_id, page=page)
            player_watch_times = response["results"]
            all_player_watch_times.extend(player_watch_times)
            if not response["next"]:
                break
            page += 1
        return {"results": all_player_watch_times}

    async def fetch_player_player_watch_time(
        self, player_id: str, player_watch_time_id: str
    ) -> Dict[str, Any]:
        """
        Fetches a single watch time for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/player-watch-times/{player_watch_time_id}/"
        return await self.client._get(url)

    async def create_player_player_watch_time(
        self, player_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Creates a new watch time for a player.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/player-watch-times/"
        return await self.client._post(url, data)

    async def update_player_player_watch_time(
        self, player_id: str, player_watch_time_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Updates an existing watch time for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/player-watch-times/{player_watch_time_id}/"
        return await self.client._put(url, data)

    async def partial_update_player_player_watch_time(
        self, player_id: str, player_watch_time_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Partially updates an existing watch time for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/player-watch-times/{player_watch_time_id}/"
        return await self.client._patch(url, data)

    async def delete_player_player_watch_time(
        self, player_id: str, player_watch_time_id: str
    ) -> None:
        """
        Deletes an existing watch time for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/player-watch-times/{player_watch_time_id}/"
        return await self.client._delete(url)

    async def _fetch_player_points_page(
        self, player_id: str, page: Optional[int] = None, page_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of points for a player.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/points/"
        return await self.client._get(url, params=params)

    async def fetch_player_points(self, player_id: str) -> Dict[str, Any]:
        """
        Fetches all points for a player using the fetch_player_points_page method.
        """
        all_points = []
        page = 1
        while True:
            response = await self._fetch_player_points_page(player_id, page=page)
            points = response["results"]
            all_points.extend(points)
            if not response["next"]:
                break
            page += 1
        return {"results": all_points}

    async def fetch_player_point(self, player_id: str, point_id: str) -> Dict[str, Any]:
        """
        Fetches a single point for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/points/{point_id}/"
        return await self.client._get(url)

    async def create_player_point(self, player_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new point for a player.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/points/"
        return await self.client._post(url, data)

    async def update_player_point(
        self, player_id: str, point_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Updates an existing point for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/points/{point_id}/"
        return await self.client._put(url, data)

    async def partial_update_player_point(
        self, player_id: str, point_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Partially updates an existing point for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/points/{point_id}/"
        return await self.client._patch(url, data)

    async def delete_player_point(self, player_id: str, point_id: str) -> None:
        """
        Deletes an existing point for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/points/{point_id}/"
        return await self.client._delete(url)

    async def _fetch_player_raid_checkins_page(
        self, player_id: str, page: Optional[int] = None, page_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of raid check-ins for a player.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/raid-checkins/"
        return await self.client._get(url, params=params)

    async def fetch_player_raid_checkins(self, player_id: str) -> Dict[str, Any]:
        """
        Fetches all raid check-ins for a player using the fetch_player_raid_checkins_page method.
        """
        all_raid_checkins = []
        page = 1
        while True:
            response = await self._fetch_player_raid_checkins_page(player_id, page=page)
            raid_checkins = response["results"]
            all_raid_checkins.extend(raid_checkins)
            if not response["next"]:
                break
            page += 1
        return {"results": all_raid_checkins}

    async def fetch_player_raid_checkin(
        self, player_id: str, raid_checkin_id: str
    ) -> Dict[str, Any]:
        """
        Fetches a single raid check-in for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/raid-checkins/{raid_checkin_id}/"
        return await self.client._get(url)

    async def create_player_raid_checkin(
        self, player_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Creates a new raid check-in for a player.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/raid-checkins/"
        return await self.client._post(url, data)

    async def update_player_raid_checkin(
        self, player_id: str, raid_checkin_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Updates an existing raid check-in for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/raid-checkins/{raid_checkin_id}/"
        return await self.client._put(url, data)

    async def partial_update_player_raid_checkin(
        self, player_id: str, raid_checkin_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Partially updates an existing raid check-in for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/raid-checkins/{raid_checkin_id}/"
        return await self.client._patch(url, data)

    async def delete_player_raid_checkin(self, player_id: str, raid_checkin_id: str) -> None:
        """
        Deletes an existing raid check-in for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/raid-checkins/{raid_checkin_id}/"
        return await self.client._delete(url)

    async def _fetch_player_sentry_checkins_page(
        self, player_id: str, page: Optional[int] = None, page_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of sentry check-ins for a player.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/sentry-checkins/"
        return await self.client._get(url, params=params)

    async def fetch_player_sentry_checkins(self, player_id: str) -> Dict[str, Any]:
        """
        Fetches all sentry check-ins for a player using the fetch_player_sentry_checkins_page method.
        """
        all_sentry_checkins = []
        page = 1
        while True:
            response = await self._fetch_player_sentry_checkins_page(player_id, page=page)
            sentry_checkins = response["results"]
            all_sentry_checkins.extend(sentry_checkins)
            if not response["next"]:
                break
            page += 1
        return {"results": all_sentry_checkins}

    async def fetch_player_sentry_checkin(
        self, player_id: str, sentry_checkin_id: str
    ) -> Dict[str, Any]:
        """
        Fetches a single sentry check-in for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/sentry-checkins/{sentry_checkin_id}/"
        return await self.client._get(url)

    async def create_player_sentry_checkin(
        self, player_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Creates a new sentry check-in for a player.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/sentry-checkins/"
        return await self.client._post(url, data)

    async def update_player_sentry_checkin(
        self, player_id: str, sentry_checkin_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Updates an existing sentry check-in for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/sentry-checkins/{sentry_checkin_id}/"
        return await self.client._put(url, data)

    async def partial_update_player_sentry_checkin(
        self, player_id: str, sentry_checkin_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Partially updates an existing sentry check-in for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/sentry-checkins/{sentry_checkin_id}/"
        return await self.client._patch(url, data)

    async def delete_player_sentry_checkin(self, player_id: str, sentry_checkin_id: str) -> None:
        """
        Deletes an existing sentry check-in for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/sentry-checkins/{sentry_checkin_id}/"
        return await self.client._delete(url)

    async def _fetch_player_spoils_claims_page(
        self, player_id: str, page: Optional[int] = None, page_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of spoils claims for a player.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/spoils-claims/"
        return await self.client._get(url, params=params)

    async def fetch_player_spoils_claims(self, player_id: str) -> Dict[str, Any]:
        """
        Fetches all spoils claims for a player using the fetch_player_spoils_claims_page method.
        """
        all_spoils_claims = []
        page = 1
        while True:
            response = await self._fetch_player_spoils_claims_page(player_id, page=page)
            spoils_claims = response["results"]
            all_spoils_claims.extend(spoils_claims)
            if not response["next"]:
                break
            page += 1
        return {"results": all_spoils_claims}

    async def fetch_player_spoils_claim(
        self, player_id: str, spoils_claim_id: str
    ) -> Dict[str, Any]:
        """
        Fetches a single spoils claim for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/spoils-claims/{spoils_claim_id}/"
        return await self.client._get(url)

    async def create_player_spoils_claim(
        self, player_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Creates a new spoils claim for a player.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/spoils-claims/"
        return await self.client._post(url, data)

    async def update_player_spoils_claim(
        self, player_id: str, spoils_claim_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Updates an existing spoils claim for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/spoils-claims/{spoils_claim_id}/"
        return await self.client._put(url, data)

    async def partial_update_player_spoils_claim(
        self, player_id: str, spoils_claim_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Partially updates an existing spoils claim for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/spoils-claims/{spoils_claim_id}/"
        return await self.client._patch(url, data)

    async def delete_player_spoils_claim(self, player_id: str, spoils_claim_id: str) -> None:
        """
        Deletes an existing spoils claim for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/spoils-claims/{spoils_claim_id}/"
        return await self.client._delete(url)

    async def _fetch_player_subscriptions_page(
        self, player_id: str, page: Optional[int] = None, page_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of subscriptions for a player.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/subscriptions/"
        return await self.client._get(url, params=params)

    async def fetch_player_subscriptions(self, player_id: str) -> Dict[str, Any]:
        """
        Fetches all subscriptions for a player using the fetch_player_subscriptions_page method.
        """
        all_subscriptions = []
        page = 1
        while True:
            response = await self._fetch_player_subscriptions_page(player_id, page=page)
            subscriptions = response["results"]
            all_subscriptions.extend(subscriptions)
            if not response["next"]:
                break
            page += 1
        return {"results": all_subscriptions}

    async def fetch_player_subscription(
        self, player_id: str, subscription_id: str
    ) -> Dict[str, Any]:
        """
        Fetches a single subscription for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/subscriptions/{subscription_id}/"
        return await self.client._get(url)

    async def create_player_subscription(
        self, player_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Creates a new subscription for a player.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/subscriptions/"
        return await self.client._post(url, data)

    async def update_player_subscription(
        self, player_id: str, subscription_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Updates an existing subscription for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/subscriptions/{subscription_id}/"
        return await self.client._put(url, data)

    async def partial_update_player_subscription(
        self, player_id: str, subscription_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Partially updates an existing subscription for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/subscriptions/{subscription_id}/"
        return await self.client._patch(url, data)

    async def delete_player_subscription(self, player_id: str, subscription_id: str) -> None:
        """
        Deletes an existing subscription for a player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/players/{player_id}/subscriptions/{subscription_id}/"
        return await self.client._delete(url)

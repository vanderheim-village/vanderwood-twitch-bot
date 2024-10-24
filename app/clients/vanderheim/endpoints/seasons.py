from typing import Optional, Dict, Any

from app.clients.vanderheim.base_client import BaseAPIClient


class SeasonsAPI:
    def __init__(self, client: BaseAPIClient):
        self.client = client
    
    def _fetch_seasons_page(self, page: Optional[int] = None, page_size: Optional[int] = None) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of seasons.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/seasons/"
        return self.client._get(url, params=params)
    
    def fetch_all_seasons(self) -> Dict[str, Any]:
        """
        Fetches all seasons using the fetch_seasons_page method.
        """
        all_seasons = []
        page = 1
        while True:
            response = self._fetch_seasons_page(page=page)
            seasons = response["results"]
            all_seasons.extend(seasons)
            if not response["next"]:
                break
            page += 1
        return {"results": all_seasons}
    
    def fetch_season(self, season_id: int) -> Dict[str, Any]:
        """
        Fetches a single season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/"
        return self.client._get(url)
    
    def create_season(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new season.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/"
        return self.client._post(url, data)
    
    def update_season(self, season_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates an existing season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/"
        return self.client._put(url, data)
    
    def partial_update_season(self, season_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Partially updates an existing season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/"
        return self.client._patch(url, data)
    
    def delete_season(self, season_id: int) -> None:
        """
        Deletes a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/"
        self.client._delete(url)

    def _fetch_season_clan_spoils_sessions_page(self, season_id: int, page: Optional[int] = None, page_size: Optional[int] = None) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of clan spoils sessions for a season.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/clan-spoils-sessions/"
        return self.client._get(url, params=params)
    
    def fetch_season_clan_spoils_sessions(self, season_id: int) -> Dict[str, Any]:
        """
        Fetches all clan spoils sessions for a season using the fetch_season_clan_spoils_sessions_page method.
        """
        all_season_clan_spoils_sessions = []
        page = 1
        while True:
            response = self._fetch_season_clan_spoils_sessions_page(season_id, page=page)
            season_clan_spoils_sessions = response["results"]
            all_season_clan_spoils_sessions.extend(season_clan_spoils_sessions)
            if not response["next"]:
                break
            page += 1
        return {"results": all_season_clan_spoils_sessions}
    
    def fetch_season_clan_spoils_session(self, season_id: int, clan_spoils_session_id: int) -> Dict[str, Any]:
        """
        Fetches a single clan spoils session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/clan-spoils-sessions/{clan_spoils_session_id}/"
        return self.client._get(url)
    
    def create_season_clan_spoils_session(self, season_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new clan spoils session for a season.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/clan-spoils-sessions/"
        return self.client._post(url, data)
    
    def update_season_clan_spoils_session(self, season_id: int, clan_spoils_session_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates an existing clan spoils session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/clan-spoils-sessions/{clan_spoils_session_id}/"
        return self.client._put(url, data)
    
    def partial_update_season_clan_spoils_session(self, season_id: int, clan_spoils_session_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Partially updates an existing clan spoils session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/clan-spoils-sessions/{clan_spoils_session_id}/"
        return self.client._patch(url, data)
    
    def delete_season_clan_spoils_session(self, season_id: int, clan_spoils_session_id: int) -> None:
        """
        Deletes a clan spoils session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/clan-spoils-sessions/{clan_spoils_session_id}/"
        self.client._delete(url)

    def _fetch_season_clan_spoils_session_claims_page(self, season_id: int, clan_spoils_session_id: int,  page: Optional[int] = None, page_size: Optional[int] = None) -> Dict[str, Any]:
        """
        Fetch a single page of a paginated list of clan spoils claims for a clan spoils session for a season.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/clan-spoils-session/{clan_spoils_session_id}/claims/"
        return self.client._get(url, params=params)
    
    def fetch_season_clan_spoils_session_claims(self, season_id: int, clan_spoils_session_id: int) -> Dict[str, Any]:
        """
        Fetches all clan spoils claims for a clan spoils session for a season using the fetch_season_clan_spoils_session_claims_page method.
        """
        all_clan_spoils_claims = []
        page = 1
        while True:
            response = self._fetch_season_clan_spoils_session_claims_page(season_id, clan_spoils_session_id, page=page)
            clan_spoils_claims = response["results"]
            all_clan_spoils_claims.extend(clan_spoils_claims)
            if not response["next"]:
                break
            page += 1
        return {"results": all_clan_spoils_claims}
    
    def fetch_season_clan_spoils_session_claim(self, season_id: int, clan_spoils_session_id: int, clan_spoils_claim_id: int) -> Dict[str, Any]:
        """
        Fetches a single clan spoils claim for a clan spoils session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/clan-spoils-sessions/{clan_spoils_session_id}/claims/{clan_spoils_claim_id}/"
        return self.client._get(url)
    
    def create_season_clan_spoils_session_claim(self, season_id: int, clan_spoils_session_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new clan spoils claim for a clan spoils session for a season.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/clan-spoils-sessions/{clan_spoils_session_id}/claims/"
        return self.client._post(url, data)
    
    def update_season_clan_spoils_session_claim(self, season_id: int, clan_spoils_session_id: int, clan_spoils_claim_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates an existing clan spoils claim for a clan spoils session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/clan-spoils-sessions/{clan_spoils_session_id}/claims/{clan_spoils_claim_id}/"
        return self.client._put(url, data)
    
    def partial_update_season_clan_spoils_session_claim(self, season_id: int, clan_spoils_session_id: int, clan_spoils_claim_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Partially updates an existing clan spoils claim for a clan spoils session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/clan-spoils-sessions/{clan_spoils_session_id}/claims/{clan_spoils_claim_id}/"
        return self.client._patch(url, data)
    
    def delete_season_clan_spoils_session_claim(self, season_id: int, clan_spoils_session_id: int, clan_spoils_claim_id: int) -> None:
        """
        Deletes a clan spoils claim for a clan spoils session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/clan-spoils-sessions/{clan_spoils_session_id}/claims/{clan_spoils_claim_id}/"
        self.client._delete(url)
    
    def _fetch_season_points_page(self, season_id: int, page: Optional[int] = None, page_size: Optional[int] = None) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of points for a season.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/points/"
        return self.client._get(url, params=params)
    
    def fetch_season_points(self, season_id: int) -> Dict[str, Any]:
        """
        Fetches all points for a season using the fetch_season_points_page method.
        """
        all_points = []
        page = 1
        while True:
            response = self._fetch_season_points_page(season_id, page=page)
            points = response["results"]
            all_points.extend(points)
            if not response["next"]:
                break
            page += 1
        return {"results": all_points}
    
    def fetch_season_point(self, season_id: int, point_id: int) -> Dict[str, Any]:
        """
        Fetches a single point for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/points/{point_id}/"
        return self.client._get(url)
    
    def create_season_point(self, season_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new point for a season.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/points/"
        return self.client._post(url, data)
    
    def update_season_point(self, season_id: int, point_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates an existing point for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/points/{point_id}/"
        return self.client._put(url, data)
    
    def partial_update_season_point(self, season_id: int, point_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Partially updates an existing point for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/points/{point_id}/"
        return self.client._patch(url, data)
    
    def delete_season_point(self, season_id: int, point_id: int) -> None:
        """
        Deletes a point for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/points/{point_id}/"
        self.client._delete(url)
    
    def _fetch_season_raid_sessions_page(self, season_id: int, page: Optional[int] = None, page_size: Optional[int] = None) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of raid sessions for a season.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/raid-sessions/"
        return self.client._get(url, params=params)
    
    def fetch_season_raid_sessions(self, season_id: int) -> Dict[str, Any]:
        """
        Fetches all raid sessions for a season using the fetch_season_raid_sessions_page method.
        """
        all_raid_sessions = []
        page = 1
        while True:
            response = self._fetch_season_raid_sessions_page(season_id, page=page)
            raid_sessions = response["results"]
            all_raid_sessions.extend(raid_sessions)
            if not response["next"]:
                break
            page += 1
        return {"results": all_raid_sessions}
    
    def fetch_season_raid_session(self, season_id: int, raid_session_id: int) -> Dict[str, Any]:
        """
        Fetches a single raid session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/raid-sessions/{raid_session_id}/"
        return self.client._get(url)
    
    def create_season_raid_session(self, season_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new raid session for a season.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/raid-sessions/"
        return self.client._post(url, data)
    
    def update_season_raid_session(self, season_id: int, raid_session_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates an existing raid session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/raid-sessions/{raid_session_id}/"
        return self.client._put(url, data)
    
    def partial_update_season_raid_session(self, season_id: int, raid_session_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Partially updates an existing raid session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/raid-sessions/{raid_session_id}/"
        return self.client._patch(url, data)
    
    def delete_season_raid_session(self, season_id: int, raid_session_id: int) -> None:
        """
        Deletes a raid session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/raid-sessions/{raid_session_id}/"
        self.client._delete(url)

    def _fetch_season_raid_session_checkins_page(self, season_id: int, raid_session_id: int, page: Optional[int] = None, page_size: Optional[int] = None) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of raid checkins for a raid session for a season.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/raid-sessions/{raid_session_id}/checkins/"
        return self.client._get(url, params=params)
    
    def fetch_season_raid_session_checkins(self, season_id: int, raid_session_id: int) -> Dict[str, Any]:
        """
        Fetches all raid checkins for a raid session for a season using the fetch_season_raid_session_checkins_page method.
        """
        all_raid_checkins = []
        page = 1
        while True:
            response = self._fetch_season_raid_session_checkins_page(season_id, raid_session_id, page=page)
            raid_checkins = response["results"]
            all_raid_checkins.extend(raid_checkins)
            if not response["next"]:
                break
            page += 1
        return {"results": all_raid_checkins}
    
    def fetch_season_raid_session_checkin(self, season_id: int, raid_session_id: int, raid_checkin_id: int) -> Dict[str, Any]:
        """
        Fetches a single raid checkin for a raid session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/raid-sessions/{raid_session_id}/checkins/{raid_checkin_id}/"
        return self.client._get(url)
    
    def create_season_raid_session_checkin(self, season_id: int, raid_session_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new raid checkin for a raid session for a season.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/raid-sessions/{raid_session_id}/checkins/"
        return self.client._post(url, data)
    
    def update_season_raid_session_checkin(self, season_id: int, raid_session_id: int, raid_checkin_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates an existing raid checkin for a raid session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/raid-sessions/{raid_session_id}/checkins/{raid_checkin_id}/"
        return self.client._put(url, data)
    
    def partial_update_season_raid_session_checkin(self, season_id: int, raid_session_id: int, raid_checkin_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Partially updates an existing raid checkin for a raid session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/raid-sessions/{raid_session_id}/checkins/{raid_checkin_id}/"
        return self.client._patch(url, data)
    
    def delete_season_raid_session_checkin(self, season_id: int, raid_session_id: int, raid_checkin_id: int) -> None:
        """
        Deletes a raid checkin for a raid session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/raid-sessions/{raid_session_id}/checkins/{raid_checkin_id}/"
        self.client._delete(url)
    
    def _fetch_season_sentry_sessions_page(self, season_id: int, page: Optional[int] = None, page_size: Optional[int] = None) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of sentry sessions for a season.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/sentry-sessions/"
        return self.client._get(url, params=params)
    
    def fetch_season_sentry_sessions(self, season_id: int) -> Dict[str, Any]:
        """
        Fetches all sentry sessions for a season using the fetch_season_sentry_sessions_page method.
        """
        all_sentry_sessions = []
        page = 1
        while True:
            response = self._fetch_season_sentry_sessions_page(season_id, page=page)
            sentry_sessions = response["results"]
            all_sentry_sessions.extend(sentry_sessions)
            if not response["next"]:
                break
            page += 1
        return {"results": all_sentry_sessions}
    
    def fetch_season_sentry_session(self, season_id: int, sentry_session_id: int) -> Dict[str, Any]:
        """
        Fetches a single sentry session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/sentry-sessions/{sentry_session_id}/"
        return self.client._get(url)
    
    def create_season_sentry_session(self, season_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new sentry session for a season.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/sentry-sessions/"
        return self.client._post(url, data)
    
    def update_season_sentry_session(self, season_id: int, sentry_session_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates an existing sentry session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/sentry-sessions/{sentry_session_id}/"
        return self.client._put(url, data)
    
    def partial_update_season_sentry_session(self, season_id: int, sentry_session_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Partially updates an existing sentry session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/sentry-sessions/{sentry_session_id}/"
        return self.client._patch(url, data)
    
    def delete_season_sentry_session(self, season_id: int, sentry_session_id: int) -> None:
        """
        Deletes a sentry session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/sentry-sessions/{sentry_session_id}/"
        self.client._delete(url)
    
    def _fetch_season_sentry_session_checkins_page(self, season_id: int, sentry_session_id: int, page: Optional[int] = None, page_size: Optional[int] = None) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of sentry checkins for a sentry session for a season.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/sentry-sessions/{sentry_session_id}/checkins/"
        return self.client._get(url, params=params)
    
    def fetch_season_sentry_session_checkins(self, season_id: int, sentry_session_id: int) -> Dict[str, Any]:
        """
        Fetches all sentry checkins for a sentry session for a season using the fetch_season_sentry_session_checkins_page method.
        """
        all_sentry_checkins = []
        page = 1
        while True:
            response = self._fetch_season_sentry_session_checkins_page(season_id, sentry_session_id, page=page)
            sentry_checkins = response["results"]
            all_sentry_checkins.extend(sentry_checkins)
            if not response["next"]:
                break
            page += 1
        return {"results": all_sentry_checkins}
    
    def fetch_season_sentry_session_checkin(self, season_id: int, sentry_session_id: int, sentry_checkin_id: int) -> Dict[str, Any]:
        """
        Fetches a single sentry checkin for a sentry session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/sentry-sessions/{sentry_session_id}/checkins/{sentry_checkin_id}/"
        return self.client._get(url)
    
    def create_season_sentry_session_checkin(self, season_id: int, sentry_session_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new sentry checkin for a sentry session for a season.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/sentry-sessions/{sentry_session_id}/checkins/"
        return self.client._post(url, data)
    
    def update_season_sentry_session_checkin(self, season_id: int, sentry_session_id: int, sentry_checkin_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates an existing sentry checkin for a sentry session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/sentry-sessions/{sentry_session_id}/checkins/{sentry_checkin_id}/"
        return self.client._put(url, data)
    
    def partial_update_season_sentry_session_checkin(self, season_id: int, sentry_session_id: int, sentry_checkin_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Partially updates an existing sentry checkin for a sentry session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/sentry-sessions/{sentry_session_id}/checkins/{sentry_checkin_id}/"
        return self.client._patch(url, data)
    
    def delete_season_sentry_session_checkin(self, season_id: int, sentry_session_id: int, sentry_checkin_id: int) -> None:
        """
        Deletes a sentry checkin for a sentry session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/sentry-sessions/{sentry_session_id}/checkins/{sentry_checkin_id}/"
        self.client._delete(url)

    def _fetch_season_sessions_page(self, season_id: int, page: Optional[int] = None, page_size: Optional[int] = None) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of sessions for a season.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/sessions/"
        return self.client._get(url, params=params)
    
    def fetch_season_sessions(self, season_id: int) -> Dict[str, Any]:
        """
        Fetches all sessions for a season using the fetch_season_sessions_page method.
        """
        all_sessions = []
        page = 1
        while True:
            response = self._fetch_season_sessions_page(season_id, page=page)
            sessions = response["results"]
            all_sessions.extend(sessions)
            if not response["next"]:
                break
            page += 1
        return {"results": all_sessions}
    
    def fetch_season_session(self, season_id: int, session_id: int) -> Dict[str, Any]:
        """
        Fetches a single session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/sessions/{session_id}/"
        return self.client._get(url)
    
    def create_season_session(self, season_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new session for a season.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/sessions/"
        return self.client._post(url, data)
    
    def update_season_session(self, season_id: int, session_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates an existing session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/sessions/{session_id}/"
        return self.client._put(url, data)
    
    def partial_update_season_session(self, season_id: int, session_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Partially updates an existing session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/sessions/{session_id}/"
        return self.client._patch(url, data)
    
    def delete_season_session(self, season_id: int, session_id: int) -> None:
        """
        Deletes a session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/sessions/{session_id}/"
        self.client._delete(url)
    
    def _fetch_season_session_checkins_page(self, season_id: int, session_id: int, page: Optional[int] = None, page_size: Optional[int] = None) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of checkins for a session for a season.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/sessions/{session_id}/checkins/"
        return self.client._get(url, params=params)
    
    def fetch_season_session_checkins(self, season_id: int, session_id: int) -> Dict[str, Any]:
        """
        Fetches all checkins for a session for a season using the fetch_season_session_checkins_page method.
        """
        all_checkins = []
        page = 1
        while True:
            response = self._fetch_season_session_checkins_page(season_id, session_id, page=page)
            checkins = response["results"]
            all_checkins.extend(checkins)
            if not response["next"]:
                break
            page += 1
        return {"results": all_checkins}
    
    def fetch_season_session_checkin(self, season_id: int, session_id: int, checkin_id: int) -> Dict[str, Any]:
        """
        Fetches a single checkin for a session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/sessions/{session_id}/checkins/{checkin_id}/"
        return self.client._get(url)
    
    def create_season_session_checkin(self, season_id: int, session_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new checkin for a session for a season.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/sessions/{session_id}/checkins/"
        return self.client._post(url, data)
    
    def update_season_session_checkin(self, season_id: int, session_id: int, checkin_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates an existing checkin for a session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/sessions/{session_id}/checkins/{checkin_id}/"
        return self.client._put(url, data)
    
    def partial_update_season_session_checkin(self, season_id: int, session_id: int, checkin_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Partially updates an existing checkin for a session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/sessions/{session_id}/checkins/{checkin_id}/"
        return self.client._patch(url, data)
    
    def delete_season_session_checkin(self, season_id: int, session_id: int, checkin_id: int) -> None:
        """
        Deletes a checkin for a session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/sessions/{session_id}/checkins/{checkin_id}/"
        self.client._delete(url)
    
    def _fetch_season_spoils_sessions_page(self, season_id: int, page: Optional[int] = None, page_size: Optional[int] = None) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of spoils sessions for a season.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/spoils-sessions/"
        return self.client._get(url, params=params)
    
    def fetch_season_spoils_sessions(self, season_id: int) -> Dict[str, Any]:
        """
        Fetches all spoils sessions for a season using the fetch_season_spoils_sessions_page method.
        """
        all_spoils_sessions = []
        page = 1
        while True:
            response = self._fetch_season_spoils_sessions_page(season_id, page=page)
            spoils_sessions = response["results"]
            all_spoils_sessions.extend(spoils_sessions)
            if not response["next"]:
                break
            page += 1
        return {"results": all_spoils_sessions}
    
    def fetch_season_spoils_session(self, season_id: int, spoils_session_id: int) -> Dict[str, Any]:
        """
        Fetches a single spoils session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/spoils-sessions/{spoils_session_id}/"
        return self.client._get(url)
    
    def create_season_spoils_session(self, season_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new spoils session for a season.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/spoils-sessions/"
        return self.client._post(url, data)
    
    def update_season_spoils_session(self, season_id: int, spoils_session_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates an existing spoils session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/spoils-sessions/{spoils_session_id}/"
        return self.client._put(url, data)
    
    def partial_update_season_spoils_session(self, season_id: int, spoils_session_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Partially updates an existing spoils session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/spoils-sessions/{spoils_session_id}/"
        return self.client._patch(url, data)
    
    def delete_season_spoils_session(self, season_id: int, spoils_session_id: int) -> None:
        """
        Deletes a spoils session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/spoils-sessions/{spoils_session_id}/"
        self.client._delete(url)

    def _fetch_season_spoils_session_claims_page(self, season_id: int, spoils_session_id: int, page: Optional[int] = None, page_size: Optional[int] = None) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of spoils claims for a spoils session for a season.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/spoils-sessions/{spoils_session_id}/claims/"
        return self.client._get(url, params=params)
    
    def fetch_season_spoils_session_claims(self, season_id: int, spoils_session_id: int) -> Dict[str, Any]:
        """
        Fetches all spoils claims for a spoils session for a season using the fetch_season_spoils_session_claims_page method.
        """
        all_spoils_claims = []
        page = 1
        while True:
            response = self._fetch_season_spoils_session_claims_page(season_id, spoils_session_id, page=page)
            spoils_claims = response["results"]
            all_spoils_claims.extend(spoils_claims)
            if not response["next"]:
                break
            page += 1
        return {"results": all_spoils_claims}
    
    def fetch_season_spoils_session_claim(self, season_id: int, spoils_session_id: int, spoils_claim_id: int) -> Dict[str, Any]:
        """
        Fetches a single spoils claim for a spoils session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/spoils-sessions/{spoils_session_id}/claims/{spoils_claim_id}/"
        return self.client._get(url)
    
    def create_season_spoils_session_claim(self, season_id: int, spoils_session_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new spoils claim for a spoils session for a season.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/spoils-sessions/{spoils_session_id}/claims/"
        return self.client._post(url, data)
    
    def update_season_spoils_session_claim(self, season_id: int, spoils_session_id: int, spoils_claim_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates an existing spoils claim for a spoils session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/spoils-sessions/{spoils_session_id}/claims/{spoils_claim_id}/"
        return self.client._put(url, data)
    
    def partial_update_season_spoils_session_claim(self, season_id: int, spoils_session_id: int, spoils_claim_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Partially updates an existing spoils claim for a spoils session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/spoils-sessions/{spoils_session_id}/claims/{spoils_claim_id}/"
        return self.client._patch(url, data)
    
    def delete_season_spoils_session_claim(self, season_id: int, spoils_session_id: int, spoils_claim_id: int) -> None:
        """
        Deletes a spoils claim for a spoils session for a season by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/seasons/{season_id}/spoils-sessions/{spoils_session_id}/claims/{spoils_claim_id}/"
        self.client._delete(url)

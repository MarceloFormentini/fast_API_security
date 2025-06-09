def test_valid_fingerprint(client, auth_cookies):
    headers = {"Authorization": f"Bearer {auth_cookies['token']}",
               "User-Agent": "test-agent"}
    res = client.get("/teams", headers=headers, cookies=auth_cookies['cookies'])
    assert res.status_code == 200


def test_invalid_fingerprint(client, auth_cookies):
    headers = {"Authorization": f"Bearer {auth_cookies['token']}",
               "User-Agent": "evil-agent"}
    res = client.get("/teams", headers=headers, cookies=auth_cookies['cookies'])
    assert res.status_code == 401
def test_missing_csrf_header(client, auth_cookies):
    # tenta criar time sem X-CSRF-Token
    res = client.post("/teams", json={"code":"T1","name":"Team1"},
                      cookies=auth_cookies['cookies'])
    assert res.status_code == 403


def test_mismatched_csrf_header(client, auth_cookies):
    res = client.post(
        "/teams",
        json={"code":"T2","name":"Team2"},
        headers={"X-CSRF-Token": "wrong"},
        cookies=auth_cookies['cookies']
    )
    assert res.status_code == 403


def test_valid_csrf(client, auth_cookies):
    csrf = auth_cookies['cookies'].get('csrf_token')
    res = client.post(
        "/teams",
        json={"code":"T3","name":"Team3"},
        headers={"X-CSRF-Token": csrf},
        cookies=auth_cookies['cookies']
    )
    assert res.status_code == 201
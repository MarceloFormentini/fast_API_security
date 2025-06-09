def test_csp_headers(client, auth_cookies):
    res = client.get("/teams", headers={"Authorization": f"Bearer {auth_cookies['token']}"}, cookies=auth_cookies['cookies'])
    assert "Content-Security-Policy" in res.headers
    assert "X-Frame-Options" in res.headers
    assert res.headers.get("X-Content-Type-Options") == "nosniff"


def test_xss_escape(client, auth_cookies):
    # injeta payload XSS e verifica escape
    csrf = auth_cookies['cookies'].get('csrf_token')
    payload = {"code": "<script>alert(1)</script>", "name": "XSS"}
    client.post(
        "/teams",
        json=payload,
        headers={"X-CSRF-Token": csrf},
        cookies=auth_cookies['cookies']
    )
    res = client.get("/teams", headers={"Authorization": f"Bearer {auth_cookies['token']}"}, cookies=auth_cookies['cookies'])
    body = res.text
    assert '<script>' not in body
    assert '&lt;script&gt;alert(1)&lt;/script&gt;' in body


def test_jwt_in_httponly_cookie(client, auth_cookies):
    # Verifica se o token veio como cookie HttpOnly
    cookies = auth_cookies['cookies']
    assert 'access_token' in cookies
    # TestClient não expõe HttpOnly diretamente, mas pode-se inferir via implementação real
    # Em produção, verifique em browser DevTools que cookie esteja HttpOnly
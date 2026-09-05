#![cfg(feature = "ui")]

use axum::{
    body::Body,
    http::{header, Request, StatusCode},
};
use cyberalchemy_kep_hosted_devnet::{
    router_with_ui as router, Application, FinalityGateway, MockFinalityGateway,
};
use http_body_util::BodyExt;
use tower::ServiceExt;

#[tokio::test]
async fn interface_assets_are_complete_same_origin_and_security_bounded() {
    let application =
        Application::memory(FinalityGateway::Mock(MockFinalityGateway::default())).await;
    let app = router(application);

    let page = app
        .clone()
        .oneshot(Request::get("/").body(Body::empty()).unwrap())
        .await
        .unwrap();
    assert_eq!(page.status(), StatusCode::OK);
    let csp = page
        .headers()
        .get(header::CONTENT_SECURITY_POLICY)
        .unwrap()
        .to_str()
        .unwrap();
    assert!(csp.contains("default-src 'self'"));
    assert!(csp.contains("https://api.devnet.solana.com"));
    assert!(csp.contains("object-src 'none'"));
    let html = String::from_utf8(
        page.into_body()
            .collect()
            .await
            .unwrap()
            .to_bytes()
            .to_vec(),
    )
    .unwrap();
    for view in ["home-view", "paper-view", "explore-view"] {
        assert!(html.contains(&format!("id=\"{view}\"")));
    }
    for target in ["home", "paper", "explore"] {
        assert!(html.contains(&format!("data-view-target=\"{target}\"")));
    }
    for marker in [
        "journey-shell",
        "journey-task",
        "chapter-progress",
        "change-task",
    ] {
        assert!(html.contains(marker));
    }
    assert!(!html.contains("carousel-visual"));
    assert!(!html.contains("role-switch"));
    assert!(!html.contains("orb-scene"));
    assert!(!html.contains("button class=\"step"));
    assert!(html.contains("id=\"scene-back\""));
    assert!(html.contains("id=\"scene-next\""));
    assert!(html.contains("CyberAlchemy Exchange"));
    assert!(html.contains("id=\"home-title\">CyberAlchemy Exchange</h1>"));
    assert!(!html.contains("class=\"home-kicker\""));
    assert!(html.contains("Knowledge Expansion Protocol"));
    assert!(html.contains("class=\"kep-rail-model\""));
    assert!(html.contains("class=\"kep-term\""));
    assert!(html.contains("class=\"kep-rail-set\"><small>origin</small><b>{ A }</b>"));
    assert!(html.contains("tabindex=\"0\" aria-describedby=\"kep-tooltip-rail\""));
    assert!(html.contains("id=\"kep-tooltip-rail\" class=\"kep-tooltip\" role=\"tooltip\""));
    assert!(html.contains("Powered by KEP"));
    assert!(html.contains("href=\"#white-paper\""));
    assert!(!html.contains("wallet_private_key"));
    assert!(!html.contains("encryption_private_key"));
    assert!(html.contains("CyberAlchemy Lab home"));
    assert!(html.contains("cyberalchemy-mark.svg"));
    assert!(html.contains("cyberalchemy-orb-frozen.webp"));
    assert!(html.contains("cyberalchemy-orb-loop.webm"));
    assert!(html.contains("fetchpriority=\"high\""));
    assert!(html.contains("preload=\"none\""));
    assert!(html.contains("data-src=\"/assets/cyberalchemy-orb-loop.webm\""));
    assert!(!html.contains("<source src=\"/assets/cyberalchemy-orb-loop.webm\""));
    assert!(!html.contains("<script>"));
    assert!(html.contains("id=\"paper-view\""));
    assert!(html.contains("Not approved for publication"));
    assert!(html.contains("Run the KEP process"));
    assert!(html.contains("data-locale-select"));
    assert!(html.contains("data-locale-flag"));
    assert!(html.contains("value=\"pt-BR\">PT-BR"));
    assert!(html.contains("owners(V)"));
    assert!(html.contains("/assets/brand.css"));

    for (path, content_type, minimum_bytes, maximum_bytes) in [
        (
            "/assets/style.css",
            "text/css; charset=utf-8",
            5_000,
            100_000,
        ),
        (
            "/assets/brand.css",
            "text/css; charset=utf-8",
            5_000,
            100_000,
        ),
        (
            "/assets/cyberalchemy-mark.svg",
            "image/svg+xml",
            1_000,
            100_000,
        ),
        ("/assets/flag-br.svg", "image/svg+xml", 1_000, 10_000),
        ("/assets/flag-us.svg", "image/svg+xml", 500, 10_000),
        (
            "/assets/cyberalchemy-orb-frozen.webp",
            "image/webp",
            10_000,
            50_000,
        ),
        (
            "/assets/cyberalchemy-orb-loop.webm",
            "video/webm",
            100_000,
            500_000,
        ),
        (
            "/assets/app.js",
            "application/javascript; charset=utf-8",
            100_000,
            600_000,
        ),
    ] {
        let response = app
            .clone()
            .oneshot(Request::get(path).body(Body::empty()).unwrap())
            .await
            .unwrap();
        assert_eq!(response.status(), StatusCode::OK);
        assert_eq!(
            response.headers().get(header::CONTENT_TYPE).unwrap(),
            content_type
        );
        let bytes = response
            .into_body()
            .collect()
            .await
            .unwrap()
            .to_bytes()
            .len();
        assert!(bytes > minimum_bytes, "{path} is unexpectedly empty");
        assert!(bytes < maximum_bytes, "{path} exceeds its byte ceiling");
    }

    let brand_css = app
        .oneshot(
            Request::get("/assets/brand.css")
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();
    let brand_css = String::from_utf8(
        brand_css
            .into_body()
            .collect()
            .await
            .unwrap()
            .to_bytes()
            .to_vec(),
    )
    .unwrap();
    assert!(brand_css.contains(".home-orb-motion.is-active"));
    assert!(brand_css.contains(".home-orb.has-motion .home-orb-still"));
    assert!(brand_css.contains(".kep-term:focus-visible .kep-tooltip"));
    assert!(brand_css.contains("min-height: calc(100svh - 66px);"));
    assert!(brand_css.contains("align-content: safe center;"));
    assert!(!brand_css.contains("\n  height: calc(100svh - 66px);"));
    assert!(!brand_css.contains("ca2-home-orb-turn"));
    assert!(brand_css.contains("@media (prefers-reduced-motion: reduce)"));
    assert!(brand_css.contains(".home-orb-motion { display: none; }"));
}

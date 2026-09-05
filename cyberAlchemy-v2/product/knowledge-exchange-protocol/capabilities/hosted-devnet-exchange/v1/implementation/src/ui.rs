//! Optional participant workbench delivery.
//!
//! This module is deliberately excluded from the default protocol build and
//! from the protocol implementation binding. Enable the `ui` Cargo feature to
//! compose these routes with the protocol API.

use axum::{
    http::{header, HeaderValue},
    response::{Html, IntoResponse, Response},
    routing::get,
    Router,
};

use crate::{api::router, Application};

pub fn router_with_ui(application: Application) -> Router {
    router(application).merge(
        Router::new()
            .route("/", get(index))
            .route("/assets/style.css", get(styles))
            .route("/assets/brand.css", get(brand_styles))
            .route("/assets/cyberalchemy-mark.svg", get(cyberalchemy_mark))
            .route("/assets/flag-br.svg", get(flag_br))
            .route("/assets/flag-us.svg", get(flag_us))
            .route(
                "/assets/cyberalchemy-orb-frozen.webp",
                get(cyberalchemy_orb_frozen_webp),
            )
            .route(
                "/assets/cyberalchemy-orb-loop.webm",
                get(cyberalchemy_orb_loop_webm),
            )
            .route("/assets/app.js", get(client_script)),
    )
}

async fn index() -> Response {
    let mut response = Html(include_str!("../static/index.html")).into_response();
    response.headers_mut().insert(
        header::CONTENT_SECURITY_POLICY,
        HeaderValue::from_static(
            "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self' https://api.devnet.solana.com wss://api.devnet.solana.com; img-src 'self' data:; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'",
        ),
    );
    response
}

async fn styles() -> impl IntoResponse {
    (
        [(header::CONTENT_TYPE, "text/css; charset=utf-8")],
        include_str!("../static/assets/style.css"),
    )
}

async fn brand_styles() -> impl IntoResponse {
    (
        [(header::CONTENT_TYPE, "text/css; charset=utf-8")],
        include_str!("../static/assets/brand.css"),
    )
}

async fn cyberalchemy_mark() -> impl IntoResponse {
    (
        [(header::CONTENT_TYPE, "image/svg+xml")],
        include_str!("../../../../../../../../arcanum/docs/assets/cyberalchemy-mark.svg"),
    )
}

async fn flag_br() -> impl IntoResponse {
    (
        [(header::CONTENT_TYPE, "image/svg+xml")],
        include_str!("../static/assets/flag-br.svg"),
    )
}

async fn flag_us() -> impl IntoResponse {
    (
        [(header::CONTENT_TYPE, "image/svg+xml")],
        include_str!("../static/assets/flag-us.svg"),
    )
}

async fn cyberalchemy_orb_frozen_webp() -> impl IntoResponse {
    (
        [(header::CONTENT_TYPE, "image/webp")],
        include_bytes!("../static/assets/cyberalchemy-orb-frozen.webp").as_slice(),
    )
}

async fn cyberalchemy_orb_loop_webm() -> impl IntoResponse {
    (
        [(header::CONTENT_TYPE, "video/webm")],
        include_bytes!("../static/assets/cyberalchemy-orb-loop.webm").as_slice(),
    )
}

async fn client_script() -> impl IntoResponse {
    (
        [(
            header::CONTENT_TYPE,
            "application/javascript; charset=utf-8",
        )],
        include_str!("../static/assets/app.js"),
    )
}

ADR-002: Autenticación JWT
    • Contexto: Se requiere control de sesiones sin mantener cookies.
    • Decisión: Usar JSON Web Tokens con DRF SimpleJWT.
    • Alternativas: Sesiones nativas, OAuth2.
    • Consecuencias: (+) Escalable, (-) Requiere expiración y refresh tokens.
    • Estado: Aprobado.
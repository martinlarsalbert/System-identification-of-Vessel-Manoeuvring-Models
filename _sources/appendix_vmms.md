## Vessel Manoeuvring Models
### vmm_abkowitz

$$
\begin{align*}
\operatorname{X_{D}}{\left(u,v,r,\delta,T \right)} = & X_{\delta\delta} \delta^{2} + X_{r\delta} \delta r + X_{rr} r^{2} + X_{T} T + X_{u\delta\delta} \delta^{2} u + X_{ur\delta} \delta r u \\
& + X_{urr} r^{2} u + X_{uuu} u^{3} + X_{uu} u^{2} + X_{uv\delta} \delta u v + X_{uvr} r u v + X_{uvv} u v^{2} \\
& + X_{u} u + X_{v\delta} \delta v + X_{vr} r v + X_{vv} v^{2} 
\end{align*}
$$ (eq_X_D_vmm_abkowitz)



$$
\begin{align*}
\operatorname{Y_{D}}{\left(u,v,r,\delta,T \right)} = & Y_{0uu} u^{2} + Y_{0u} u + Y_{0} + Y_{\delta\delta\delta} \delta^{3} + Y_{\delta} \delta + Y_{r\delta\delta} \delta^{2} r \\
& + Y_{rr\delta} \delta r^{2} + Y_{rrr} r^{3} + Y_{r} r + Y_{u\delta} \delta u + Y_{ur} r u + Y_{uu\delta} \delta u^{2} \\
& + Y_{uur} r u^{2} + Y_{uuv} u^{2} v + Y_{uv} u v + Y_{v\delta\delta} \delta^{2} v + Y_{vr\delta} \delta r v + Y_{vrr} r^{2} v \\
& + Y_{vv\delta} \delta v^{2} + Y_{vvr} r v^{2} + Y_{vvv} v^{3} + Y_{v} v 
\end{align*}
$$ (eq_Y_D_vmm_abkowitz)



$$
\begin{align*}
\operatorname{N_{D}}{\left(u,v,r,\delta,T \right)} = & N_{0uu} u^{2} + N_{0u} u + N_{0} + N_{\delta\delta\delta} \delta^{3} + N_{\delta} \delta + N_{r\delta\delta} \delta^{2} r \\
& + N_{rr\delta} \delta r^{2} + N_{rrr} r^{3} + N_{r} r + N_{u\delta} \delta u + N_{ur} r u + N_{uu\delta} \delta u^{2} \\
& + N_{uur} r u^{2} + N_{uuv} u^{2} v + N_{uv} u v + N_{v\delta\delta} \delta^{2} v + N_{vr\delta} \delta r v + N_{vrr} r^{2} v \\
& + N_{vv\delta} \delta v^{2} + N_{vvr} r v^{2} + N_{vvv} v^{3} + N_{v} v 
\end{align*}
$$ (eq_N_D_vmm_abkowitz)


### vmm_abkowitz_simple

$$
\begin{align*}
\operatorname{X_{D}}{\left(u,v,r,\delta,T \right)} = & X_{rr} r^{2} + X_{T} T + X_{uuu} u^{3} + X_{uu} u^{2} + X_{uvr} r u v + X_{uvv} u v^{2} \\
& + X_{vr} r v + X_{vv} v^{2} 
\end{align*}
$$ (eq_X_D_vmm_abkowitz_simple)



$$
\begin{align*}
\operatorname{Y_{D}}{\left(u,v,r,\delta,T \right)} = & Y_{\delta\delta\delta} \delta^{3} + Y_{\delta} \delta + Y_{r} r + Y_{u\delta} \delta u + Y_{ur} r u + Y_{uu\delta} \delta u^{2} \\
& + Y_{uuv} u^{2} v + Y_{uv} u v + Y_{v} v 
\end{align*}
$$ (eq_Y_D_vmm_abkowitz_simple)



$$
\begin{align*}
\operatorname{N_{D}}{\left(u,v,r,\delta,T \right)} = & N_{\delta\delta\delta} \delta^{3} + N_{\delta} \delta + N_{r} r + N_{u\delta} \delta u + N_{ur} r u + N_{uu\delta} \delta u^{2} \\
& + N_{uuv} u^{2} v + N_{uv} u v + N_{v} v 
\end{align*}
$$ (eq_N_D_vmm_abkowitz_simple)


### vmm_martin

$$
\begin{align*}
\operatorname{X_{D}}{\left(u,v,r,\delta,T \right)} = & X_{\delta\delta} \delta^{2} + X_{rr} r^{2} + X_{T} T + X_{uu} u^{2} + X_{u} u + X_{v\delta} \delta v \\
& + X_{vr} r v 
\end{align*}
$$ (eq_X_D_vmm_martin)



$$
\begin{align*}
\operatorname{Y_{D}}{\left(u,v,r,\delta,T \right)} = & Y_{\delta} \delta + Y_{r\delta\delta} \delta^{2} r + Y_{r} r + Y_{ur} r u + Y_{uv} u v + Y_{u} u \\
& + Y_{v\delta\delta} \delta^{2} v + Y_{v} v 
\end{align*}
$$ (eq_Y_D_vmm_martin)



$$
\begin{align*}
\operatorname{N_{D}}{\left(u,v,r,\delta,T \right)} = & N_{\delta} \delta + N_{r\delta\delta} \delta^{2} r + N_{r} r + N_{ur} r u + N_{uv} u v + N_{u} u \\
& + N_{v\delta\delta} \delta^{2} v + N_{v} v 
\end{align*}
$$ (eq_N_D_vmm_martin)


### vmm_linear

$$
\begin{align*}
\operatorname{X_{D}}{\left(u,v,r,\delta,T \right)} = & X_{\delta} \delta + X_{r} r + X_{u} u + X_{v} v 
\end{align*}
$$ (eq_X_D_vmm_linear)



$$
\begin{align*}
\operatorname{Y_{D}}{\left(u,v,r,\delta,T \right)} = & Y_{\delta} \delta + Y_{r} r + Y_{u} u + Y_{v} v 
\end{align*}
$$ (eq_Y_D_vmm_linear)



$$
\begin{align*}
\operatorname{N_{D}}{\left(u,v,r,\delta,T \right)} = & N_{\delta} \delta + N_{r} r + N_{u} u + N_{v} v 
\end{align*}
$$ (eq_N_D_vmm_linear)


### vmm_martins_simple

$$
\begin{align*}
\operatorname{X_{D}}{\left(u,v,r,\delta,T \right)} = & X_{\delta\delta} \delta^{2} + X_{rr} r^{2} + X_{T} T + X_{u} u + X_{vr} r v 
\end{align*}
$$ (eq_X_D_vmm_martins_simple)



$$
\begin{align*}
\operatorname{Y_{D}}{\left(u,v,r,\delta,T \right)} = & Y_{\delta} \delta + Y_{r} r + Y_{ur} r u + Y_{u} u + Y_{v} v 
\end{align*}
$$ (eq_Y_D_vmm_martins_simple)



$$
\begin{align*}
\operatorname{N_{D}}{\left(u,v,r,\delta,T \right)} = & N_{\delta} \delta + N_{r} r + N_{ur} r u + N_{u} u + N_{v} v 
\end{align*}
$$ (eq_N_D_vmm_martins_simple)


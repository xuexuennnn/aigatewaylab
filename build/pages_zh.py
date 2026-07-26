# -*- coding: utf-8 -*-
"""Simplified-Chinese page bodies (/zh/ tree). Full translations, same
structure and same honesty rules as the English tree."""

HOME_TITLE = "自托管 AI API 网关：部署与运维"
HOME_DESC = ("自托管 AI API 网关的部署、加固与运维：Docker、HTTPS、密钥管理、"
             "监控、备份与故障转移。独立演示站。")
HOME_BODY = """
<div class="hero">
<div>
<p class="kicker">部署 &middot; 加固 &middot; 运维</p>
<h1>自托管 AI API 网关<br>部署与运维</h1>
<p class="lead">我为需要统一管控 LLM 流量入口的团队部署、加固并运维自托管
AI API 网关——密钥是你的，日志是你的，基础设施也是你的。</p>
<p class="cta-row">
  <a class="btn" href="mailto:hello@aigatewaylab.xyz">联系我</a>
  <a class="btn ghost btn-gap" href="demo/">查看在线演示</a>
</p>
</div>
<div class="hero-console" aria-label="部署流程示意（静态示例）">
  <div class="hc-bar"><span class="hc-dot"></span><span class="hc-dot"></span><span class="hc-dot"></span>部署 &middot; 验证 &middot; 交接</div>
<pre><code><span class="hc-c"># 每次交付以证据收尾，而不是口头承诺</span>
<span class="hc-k">$</span> deployctl preflight --remote gateway-host
<span class="hc-o">ok</span>  80/443 空闲 &middot; docker 27.x &middot; 磁盘余 4GB
<span class="hc-k">$</span> deployctl apply --plan plan.json
<span class="hc-o">ok</span>  容器 healthy &middot; 仅绑定 127.0.0.1
<span class="hc-k">$</span> deployctl verify --target gateway-host
<span class="hc-o">ok</span>  TLS A &middot; HSTS &middot; 安全头 6/6 &middot; 日志已脱敏
<span class="hc-c"># 交接物：运维手册 + 备份 + 属于你的密钥</span></code></pre>
</div>
</div>

<h2>问题在哪</h2>
<div class="grid c3">
  <div class="card glass"><h3>密钥散落各处</h3><p class="dim">服务商 API 密钥
  被贴进 notebook、CI 变量和桌面应用。没人说得清哪把密钥在哪里被使用，
  轮换一把要付出什么代价。</p></div>
  <div class="card glass"><h3>成本不可见</h3><p class="dim">账单月底才来。
  是哪个团队、哪个功能、哪个失控脚本花掉了预算？服务商的控制台答不上来。
  </p></div>
  <div class="card glass"><h3>代码层面的厂商锁定</h3><p class="dim">
  每个服务都硬编码一家厂商的 SDK。想换模型——或者想扛过一次宕机——都得改代
  码、重新发布。</p></div>
</div>

<h2>网关解决什么</h2>
<p>自托管网关（如 LiteLLM、one-api 或 Sub2API 一类的开源项目）在你所有上游
之前提供一个 OpenAI 兼容端点。业务服务拿到的是可创建、可限额、可吊销的
<em>虚拟密钥</em>；上游密钥集中保管在一处。你获得按密钥计量的用量、速率限
制、模型路由与故障转移——全部跑在你自己的服务器上。</p>

<h2>我交付什么</h2>
<div class="grid c2">
  <div class="card"><h3>部署</h3><p class="dim">Docker Compose 或 systemd 部
  署，反向代理带 HTTPS 与 HSTS，非 root 容器，目录结构成文档，升级路径经过
  实测而不是拍脑袋。</p></div>
  <div class="card"><h3>加固</h3><p class="dim">密钥入库并收紧权限，管理面与
  数据面分离，安全响应头、fail2ban、日志脱敏——密钥永远不会以明文落进日志。
  </p></div>
  <div class="card"><h3>运维</h3><p class="dim">健康检查与告警、用量看板、备
  份与恢复演练（附成文 runbook）、按团队与按密钥的配额策略。</p></div>
  <div class="card"><h3>交接</h3><p class="dim">最终一切归你：基础设施、文档
  和一段录屏讲解。系统的运转不依赖我——这正是交付目标。</p></div>
</div>

<h2>服务边界，事先说明</h2>
<div class="notice">我部署的网关只路由<strong>你自己的服务商账号与 API 密
钥</strong>（或你的组织获得授权使用的密钥）下的流量。我不构建、不运维以下
系统：把消费级订阅转售为 API、共享或拼池账号配额、绕过服务商速率限制、提取
账号凭证。完整清单见<a href="compliance/">合规页</a>。</div>
"""

ARCH_TITLE = "网关架构"
ARCH_DESC = "自托管 AI API 网关参考架构：信任边界、数据流、密钥保管与故障域。"
ARCH_BODY = """
<h1>架构</h1>
<p class="lead">这是我部署时采用的参考布局——更重要的是，信任边界画在哪里。</p>

<h2>数据流</h2>
<div class="diagram">
 客户端（你的业务服务、内部工具）
   │  虚拟密钥 (vk-...)，永远不是服务商密钥
   ▼
┌───────────────────────────────────────────────┐
│  反向代理  (Caddy / nginx)                    │  TLS、HSTS、限流、
│  - 终结 HTTPS                                 │  安全响应头
└───────────────┬───────────────────────────────┘
                ▼
┌───────────────────────────────────────────────┐
│  网关  (LiteLLM / one-api 一类)               │
│  - 认证：虚拟密钥 → 团队、配额、模型          │
│  - 路由：模型名 → 上游池                      │
│  - 用量计量、请求日志（已脱敏）               │
│  - 故障转移：重试下一个健康上游               │
└──────┬──────────────────────────┬─────────────┘
       ▼                          ▼
┌──────────────┐          ┌──────────────┐
│ 密钥保管     │          │ SQLite/Postgres│
│ (env/文件,   │          │ 用量、密钥、   │
│  0600, 不可  │          │ 审计日志       │
│  经 web 访问)│          └──────────────┘
└──────┬───────┘
       ▼  服务商密钥 (sk-...，归你所有)
 上游服务商（OpenAI、Anthropic、Google 等官方 API）
</div>

<h2>信任边界</h2>
<table>
<tr><th>边界</th><th>规则</th></tr>
<tr><td>公网 → 代理</td><td>只暴露 443。管理界面不在公网接口上——只能经
SSH 隧道或 VPN 访问。</td></tr>
<tr><td>代理 → 网关</td><td>回环或内网。网关容器永远不绑定公网端口。</td></tr>
<tr><td>网关 → 密钥库</td><td>服务商密钥只有网关进程用户可读（0600、非
root）。它们不会出现在日志、报错信息或客户端响应里。</td></tr>
<tr><td>客户端 → 网关</td><td>客户端持有的是带配额、可吊销的虚拟密钥。某个
客户端被攻破，烧掉的是一把虚拟密钥，而不是服务商账号。</td></tr>
</table>

<h2>故障域</h2>
<ul>
<li><strong>上游宕机：</strong>健康检查把该上游标记为不健康；路由器把请求重
试到同一模型等级的下一个服务商。<a href="../case-study/">案例研究</a>里有一
条真实结构的故障转移时间线（数据为合成）。</li>
<li><strong>网关崩溃：</strong>systemd/compose 重启策略，外加外部健康探针
（形态类似我的
<a href="https://github.com/xuexuennnn/sentinel" rel="noopener">sentinel</a>
项目），在状态变化时各告警一次。</li>
<li><strong>主机丢失：</strong>数据库与配置每夜加密备份；恢复演练写入文档并
实际排练——恢复耗时取决于镜像拉取与 DNS，在交接时按环境实测，而非估算。</li>
</ul>
"""

DEMO_TITLE = "在线演示 — 模拟网关控制台"
DEMO_DESC = ("自托管 AI 网关的只读演示控制台：合成的账号、密钥、请求日志与"
             "一次故障转移回放。")
DEMO_BODY = """
<h1>演示控制台</h1>
<div class="notice"><strong>以下内容全部是合成数据。</strong>上游是模拟的，
账号和余额是假的，请求日志是生成的。本站没有连接任何真实服务商账号。状态每
15 分钟自动重置；所有写操作只作用于浏览器内的一次性副本。控制台文案保留英
文，与生产环境的终端习惯一致。</div>

<div class="demo-toolbar">
  <span class="stat">demo state: <span id="d-age">fresh</span></span>
  <button class="btn ghost" id="d-reset" type="button">重置演示状态</button>
  <button class="btn ghost" id="d-replay" type="button">回放故障转移事件</button>
</div>

<h2>上游健康度</h2>
<div id="d-upstreams" class="grid c3"></div>

<h2>虚拟密钥</h2>
<p class="dim">创建、吊销，然后观察审计日志的变化。密钥只完整显示一次，之后
只显示前缀——与生产环境同一套策略。</p>
<p><button class="btn" id="d-newkey" type="button">+ 创建虚拟密钥</button></p>
<div class="scroll-x"><table id="d-keys"></table></div>

<h2>请求日志（已脱敏，与生产一致）</h2>
<div class="scroll-x"><table id="d-log"></table></div>

<h2>审计日志</h2>
<div class="scroll-x"><table id="d-audit"></table></div>

<script src="../../static/js/demo.js" defer></script>
"""

DOCS_TITLE = "部署文档"
DOCS_DESC = ("按步骤展开：自托管 AI API 网关的 Docker 部署、HTTPS、备份、"
             "升级与监控。")
DOCS_BODY = """
<h1>部署文档</h1>
<p class="lead">这是每位客户拿到的 runbook 的公开精简版。命令真实、且在演示
所用的开源网关栈上测试过；主机名与路径为示例。</p>

<h2>1 · Docker 部署</h2>
<pre><code># docker-compose.yml（节选——完整文件见 GitHub 仓库）
services:
  gateway:
    image: ghcr.io/berriai/litellm:main-stable   # 或你选定的网关
    user: "10001:10001"            # 非 root
    read_only: true                # 只读根文件系统
    tmpfs: [/tmp]
    env_file: /srv/gateway/secrets.env   # 0600, root:root
    expose: ["4000"]               # 仅内部——不绑定公网
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://127.0.0.1:4000/health/liveliness"]
      interval: 30s
      retries: 3</code></pre>
<p>原则：网关容器从不发布宿主机端口，只有反向代理发布。密钥放在 root 所有、
0600 权限的 env 文件里，以只读方式挂载。容器以固定的非 root UID 运行，根文
件系统只读。</p>

<h2>2 · HTTPS 与自动续期</h2>
<pre><code># Caddyfile —— 8 行搞定 HTTPS、HSTS 和安全头
example.com {{
  encode gzip
  header {{
    Strict-Transport-Security "max-age=31536000; includeSubDomains"
    X-Content-Type-Options nosniff
    X-Frame-Options DENY
    Referrer-Policy strict-origin-when-cross-origin
  }}
  reverse_proxy 127.0.0.1:4000
}}</code></pre>
<p>Caddy 自动签发并续期证书。用 nginx 的话由 certbot 加 systemd 定时器完成
同样的事；两种变体仓库里都有。</p>

<h2>3 · 恢复得出来的备份才是备份</h2>
<pre><code># 每夜：导出 DB + 配置，加密，保留 14 天
sqlite3 /srv/gateway/data/gateway.db ".backup /tmp/gw.db"
tar czf - -C /srv/gateway config data | age -r "$BACKUP_PUBKEY" \\
  &gt; /backup/gateway-$(date +%F).tar.gz.age
find /backup -name "gateway-*.age" -mtime +14 -delete</code></pre>
<p>没有恢复过的备份不算备份。runbook 里包含季度恢复演练：恢复到临时目录，
在私有端口拉起第二个网关实例，跑冒烟测试，然后拆除。</p>

<h2>4 · 升级不出意外</h2>
<ol>
<li>读 release notes；确认是否有 schema 迁移。</li>
<li>快照：按上面的方式备份，记录当前镜像 digest。</li>
<li>拉新镜像、重启，盯健康端点和错误率。</li>
<li>回归：跑冒烟套件（建密钥 → 发一次对话请求 → 出现用量记录）。</li>
<li>回滚路径：上一个镜像 digest + 恢复的 DB——排练过，所以时间线是每套环境
实测得出的，不是猜的。</li>
</ol>

<h2>5 · 监控</h2>
<ul>
<li><code>/health</code> 端点由外部探针巡检，基于状态变化告警（故障一条、
恢复一条——不刷屏）。</li>
<li>主机上的磁盘、内存与证书到期检查。</li>
<li>用量异常复盘：某把虚拟密钥的突增应当是一次对话，而不是一个悬案。</li>
</ul>
"""

SEC_TITLE = "安全模型"
SEC_DESC = "自托管 AI API 网关的密钥保管、最小权限、日志脱敏与事故恢复。"
SEC_BODY = """
<h1>安全</h1>
<p class="lead">网关运维里那些在顺风演示里看不见、在事故中起决定作用的部分。</p>

<h2>密钥保管</h2>
<table>
<tr><th>秘密</th><th>放在哪里</th><th>绝不允许出现在哪里</th></tr>
<tr><td>服务商密钥 (sk-…)</td><td>宿主机上 0600 的 env 文件，或密钥管理服
务；仅网关进程用户可读</td><td>日志、报错正文、客户端响应、git、容器镜像、
明文备份</td></tr>
<tr><td>虚拟密钥 (vk-…)</td><td>在网关数据库中散列存储</td>
<td>创建之后的任何完整展示——UI 只做一次性展示，日志只记前缀</td></tr>
<tr><td>管理员凭证</td><td>密码管理器；开启 TOTP</td>
<td>共享聊天、仓库里的 .env 文件</td></tr>
</table>

<h2>最小权限</h2>
<ul>
<li>容器以专用非 root UID 运行，根文件系统只读，临时空间走 tmpfs。</li>
<li>管理面绑定 localhost；访问它需要 SSH 隧道或 VPN 成员资格。公网接口只承
载推理流量。</li>
<li>数据库用户运行期没有 DDL 权限；迁移作为独立步骤执行。</li>
<li>每个客户团队有自己的虚拟密钥，带模型白名单与预算——吊销一个客户绝不波及
另一个。</li>
</ul>

<h2>日志脱敏</h2>
<p>网关位于请求路径上，它的日志天然是个蜜罐。部署时做了如下脱敏：</p>
<ul>
<li><code>Authorization</code> 头 → <code>vk-****后4位</code></li>
<li>提示词与补全正文 → 默认只记录 token 数；除非客户为调试显式开启内容日
志，且带 TTL</li>
<li>上游报错正文 → 服务商密钥在错误到达客户端或日志之前被剥离</li>
</ul>
<p><a href="../demo/">演示</a>里的请求日志展示的正是这个形态：足够运维，
不值得偷。</p>

<h2>恢复流程（排练过的，不是纸上谈兵）</h2>
<table>
<tr><th>事故</th><th>响应</th></tr>
<tr><td>虚拟密钥泄漏</td><td>吊销该密钥（请求 fail-closed），复查其使用窗口
的审计日志，按同样策略补发新钥。爆炸半径：这把密钥的配额。</td></tr>
<tr><td>疑似服务商密钥泄漏</td><td>在服务商侧轮换，更新密钥库条目，重启网关
（重试代理挡住的几秒停机），用金丝雀请求确认。</td></tr>
<tr><td>疑似主机沦陷</td><td>冻结：先在服务商侧吊销服务商密钥——那才是王
冠。用干净镜像加加密备份重建；绝不从沦陷主机恢复可执行文件。</td></tr>
<tr><td>数据丢失</td><td>恢复昨夜加密转储；转储之后的用量记录确认丢失并如实
承认——账务以服务商控制台对账。</td></tr>
</table>
"""

CASE_TITLE = "案例研究：迁移、路由与故障转移"
CASE_DESC = ("一次匿名化的网关交付：收拢散落的 API 密钥、增加模型路由，并"
             "扛过一次上游宕机。")
CASE_BODY = """
<h1>案例研究</h1>
<div class="notice">由真实的自托管网关运维工作匿名化、泛化而来。身份信息、
主机名、精确数字与厂商组合均已修改；时间线结构与故障模式才是要传达的经验。
下文数字用于说明模式，不是账单记录。</div>

<h2>起点</h2>
<p>一个小型产品团队用三个服务对接两家 AI 服务商。每个服务在自己的 env 文件
里各存一把服务商密钥；其中一把曾在一次事故中经聊天工具转发过、此后从未轮
换。没有按团队的用量视图——账单就是一个总数。</p>

<h2>阶段 1 · 收拢（第 1 周）</h2>
<ul>
<li>在内部子域名上部署网关（Docker Compose、非 root、只读根文件系统），前置
Caddy，启用 HTTPS 与 HSTS。</li>
<li>两把服务商密钥全部移入密钥库；每个服务发一把虚拟密钥，带月度预算与模型
白名单。</li>
<li>各服务只改 <code>base_url</code> 和密钥即完成切换——不改代码，因为网关
说的是同一种 API 方言。</li>
<li>在切换<em>之后</em>轮换那把经聊天泄漏的服务商密钥；客户端零改动——这正
是加一层间接的意义。</li>
</ul>

<h2>阶段 2 · 路由策略（第 2 周）</h2>
<ul>
<li>内部工具走廉价快速的模型等级，面向客户的功能走高级等级——用密钥强制执
行，而不是靠自觉。</li>
<li>按两周实测流量为每把密钥设定速率上限。</li>
<li>每夜加密备份，外部健康探针基于状态变化告警。</li>
</ul>

<h2>阶段 3 · 那次"值回票价"的宕机</h2>
<p>几周后，主力服务商出现局部故障——错误率与延迟升高（任何一家大服务商的
status page 存档里都能找到这个模式）。以下是网关视角的时间线，
<a href="../demo/">演示</a>里用合成数据复现了它：</p>
<div class="diagram">
T+0m   上游 A 错误率超阈值；健康检查将 A 标记为 degraded
T+0m   路由器开始把失败请求重试到同等级的上游 B
T+2m   探针告警一次："upstream-a: FAIL"——一条消息，不刷屏
T+31m  服务商恢复；健康检查连续两次通过；A 重回轮转
T+31m  探针告警一次："upstream-a: RECOVERED"
客户可见影响：约 2 分钟的 p95 延迟升高；没有 5xx 爆发
</div>

<h2>让它变得无聊的原因（这就是目标）</h2>
<ul>
<li>故障转移在交接时<em>做过强制故障演练</em>——事故发生时它是第二次运行，
不是第一次。</li>
<li>告警去重意味着两条消息，而不是两百条。</li>
<li>复盘只写了一段话，因为审计日志里已经有完整时间线。</li>
</ul>

<h2>交接</h2>
<p>团队拿到 runbook、恢复演练录屏和管理员权限。我的参与按设计终止；系统不
需要我也能运转——这就是交付物。</p>
"""

COMP_TITLE = "合规与边界"
COMP_DESC = ("本工作室做什么、拒绝什么：自托管 AI 网关部署的分服务商合规矩"
             "阵。")
COMP_BODY = """
<h1>合规</h1>
<p class="lead">网关技术是双刃的。管理企业自有密钥的路由技术，同样可能被滥
用于转售消费级订阅。本页白纸黑字写明：本工作室站在线的哪一边。</p>

<h2>提供的服务</h2>
<ul>
<li>部署与运维只路由<strong>你的组织自有 API 密钥</strong>（BYOK，来自服务
商官方 API 计划）流量的网关。</li>
<li>在<em>你的</em>账号范围内做虚拟密钥管理、配额、用量计量、路由与故障转
移。</li>
<li>安全加固、监控、备份与交接。</li>
</ul>

<h2>无论报酬多少都拒绝</h2>
<ul>
<li>把消费级订阅（ChatGPT Plus、Claude Pro/Max、Gemini 消费版等）转成可转售
的 API 接入。</li>
<li>账号拼池、配额共享或账号容量转售。</li>
<li>绕过服务商的速率限制、并发上限或反滥用系统。</li>
<li>提取、买卖或转移账号凭证。</li>
<li>抓取私有 Web 界面来模拟 API 访问。</li>
</ul>

<h2>服务商矩阵（API 接入方式）</h2>
<div class="notice">摘要基于 2026-07-26 阅读的服务商条款。条款会变化；在依
赖本表前请核对原文链接。这是工程合规摘要，不构成法律意见。</div>
<table>
<tr><th>服务商</th><th>官方 API（BYOK）</th><th>经网关中继消费级订阅</th>
<th>备注</th></tr>
<tr><td>OpenAI</td><td class="ok-cell">允许——平台 API 密钥</td>
<td>不允许用于第三方转售中继</td><td>平台条款将 API 用量绑定到账号持有者；
消费级 ChatGPT 条款只覆盖个人、非程序化使用。</td></tr>
<tr><td>Anthropic</td><td class="ok-cell">允许——控制台签发的 API 密钥</td>
<td>不允许用于第三方转售中继</td><td>商业条款把 API 服务与消费级 Claude 应
用区分开。</td></tr>
<tr><td>Google (Gemini)</td><td class="ok-cell">允许——AI Studio / Vertex
密钥</td><td>不允许用于第三方转售中继</td>
<td>消费级套餐与 Cloud API 是条款各自独立的两种产品。</td></tr>
<tr><td>开放权重托管（Together、Fireworks、自托管 vLLM…）</td>
<td class="ok-cell">允许——标准 API 密钥或你自己的硬件</td>
<td>n/a</td><td>对成本敏感的路由分层来说是最干净的路径。</td></tr>
</table>
<p class="dim">凡是不在服务商官方计划覆盖内的接入方式，这里一律按「未验证」
处理：本站不演示、不写成教程、也不会在 demo 中启用。</p>

<h2>关于本站</h2>
<ul>
<li><a href="../demo/">演示</a>只连接<strong>模拟上游</strong>：假账号、假
余额、假日志。这台主机上没有连接任何真实的服务商账号。</li>
<li>本站是独立的部署演示，与 Sub2API 项目及任何上游 AI 服务商均无隶属、背书
或合作关系。服务商名称仅用于描述互操作性；未使用任何 Logo。</li>
<li>部署中遵守开源网关软件的许可证——包括 LGPL-3.0-or-later 组件的源码可得
性与修改声明义务。每次交付都附许可证文本。</li>
</ul>
"""

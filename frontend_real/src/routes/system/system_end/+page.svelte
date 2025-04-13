<script>
    import axios from 'axios';
    import { onMount, onDestroy } from 'svelte';
    import '$lib/style.css';
    
    let password = "";
    let authenticated = false;
    let loading = false;
    let error = null;
    let systemData = null;
    let refreshInterval = null; // 确保初始化为null
    let autoRefresh = true;
    let lastUpdated = "";
    
    // 验证密码
    function authenticate() {
        if (password === "123456") {
            authenticated = true;
            fetchSystemData();
            setupAutoRefresh();
        } else {
            error = "密码错误，请重试";
        }
    }
    
    // 获取系统数据
    async function fetchSystemData() {
        try {
            loading = true;
            error = null;
            const response = await axios.get('http://127.0.0.1:8000/server-status');
            systemData = response.data;
            lastUpdated = new Date().toLocaleTimeString();
        } catch (err) {
            error = "获取系统数据失败: " + (err.response?.data?.detail || err.message);
        } finally {
            loading = false;
        }
    }
    
    // 设置自动刷新
    function setupAutoRefresh() {
        // 确保先清除之前的定时器
        if (refreshInterval) {
            clearInterval(refreshInterval);
            refreshInterval = null;
        }
        
        // 只有在autoRefresh为true时才设置新的定时器
        if (autoRefresh) {
            refreshInterval = setInterval(fetchSystemData, 5000);
            console.log("自动刷新已开启");
        } else {
            console.log("自动刷新已关闭");
        }
    }
    
    // 切换自动刷新
    function toggleAutoRefresh() {
        // 直接修改状态并设置刷新
        autoRefresh = !autoRefresh;
        console.log("切换自动刷新状态为:", autoRefresh);
        setupAutoRefresh();
    }
    
    // 手动刷新数据
    function refreshData() {
        fetchSystemData();
    }
    
    // 退出登录
    function logout() {
        authenticated = false;
        password = "";
        systemData = null;
        // 确保清除定时器
        if (refreshInterval) {
            clearInterval(refreshInterval);
            refreshInterval = null;
        }
    }
    
    // 组件销毁时清除定时器
    onDestroy(() => {
        if (refreshInterval) {
            clearInterval(refreshInterval);
            refreshInterval = null;
        }
    });
</script>

<div class="min-h-screen bg-base-200 p-4">
    <div class="container mx-auto px-4 py-8">
        <h1 class="text-3xl font-bold text-center mb-8"><a href="/admin/user">后端服务监控</a></h1>
        
        {#if !authenticated}
            <!-- 认证界面 -->
            <div class="card bg-base-100 shadow-xl max-w-md mx-auto">
                <div class="card-body">
                    <h2 class="card-title">请输入访问密码</h2>
                    
                    <div class="form-control w-full">
                        <input 
                            type="password" 
                            bind:value={password}
                            placeholder="请输入密码" 
                            class="input input-bordered w-full"
                            on:keypress={(e) => e.key === 'Enter' && authenticate()}
                        />
                    </div>
                    
                    <div class="card-actions justify-end mt-4">
                        <button 
                            on:click={authenticate}
                            class="btn btn-primary w-full"
                        >
                            确认
                        </button>
                    </div>
                    
                    {#if error}
                        <div class="alert alert-error mt-4">
                            <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                            <span>{error}</span>
                        </div>
                    {/if}
                </div>
            </div>
        {:else}
            <!-- 系统信息展示 -->
            <div class="mb-6 flex justify-between items-center">
                <div class="flex gap-2">
                    <button 
                        on:click={refreshData}
                        class="btn btn-primary"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd" />
                        </svg>
                        刷新数据
                    </button>
                    
                    <!-- 修改自动刷新切换控件 -->
                    <div class="form-control">
                        <label class="label cursor-pointer gap-2">
                            <span class="label-text">自动刷新</span> 
                            <input 
                                type="checkbox" 
                                class="toggle toggle-primary" 
                                checked={autoRefresh} 
                                on:click={toggleAutoRefresh} 
                            />
                        </label>
                    </div>
                </div>
                
                <div class="flex items-center gap-4">
                    {#if lastUpdated}
                        <span class="text-sm">最后更新: {lastUpdated}</span>
                    {/if}
                    <button 
                        on:click={logout}
                        class="btn btn-ghost"
                    >
                        退出
                    </button>
                </div>
            </div>
            
            {#if loading}
                <div class="flex justify-center py-8">
                    <span class="loading loading-spinner loading-lg text-primary"></span>
                </div>
            {:else if error}
                <div class="alert alert-error">
                    <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                    <span>{error}</span>
                </div>
            {:else if systemData}
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <!-- 基本状态 -->
                    <div class="card bg-base-100 shadow-xl">
                        <div class="card-body">
                            <h2 class="card-title">基本状态</h2>
                            <div class="stats stats-vertical shadow-sm">
                                <div class="stat">
                                    <div class="stat-title">状态</div>
                                    <div class="stat-value">
                                        <div class="badge badge-success">{systemData.状态}</div>
                                    </div>
                                </div>
                                <div class="stat">
                                    <div class="stat-title">时间戳</div>
                                    <div class="stat-value text-lg">{systemData.时间戳}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- 系统信息 -->
                    <div class="card bg-base-100 shadow-xl">
                        <div class="card-body">
                            <h2 class="card-title">系统信息</h2>
                            <div class="overflow-x-auto">
                                <table class="table table-zebra">
                                    <tbody>
                                        {#each Object.entries(systemData.系统信息) as [key, value]}
                                            <tr>
                                                <td class="font-medium">{key}</td>
                                                <td>{value}</td>
                                            </tr>
                                        {/each}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                    
                    <!-- 资源使用情况 -->
                    <div class="card bg-base-100 shadow-xl">
                        <div class="card-body">
                            <h2 class="card-title">资源使用情况</h2>
                            
                            <!-- CPU -->
                            <div class="collapse collapse-arrow border border-base-300 bg-base-200">
                                <input type="checkbox" checked />
                                <div class="collapse-title font-medium">
                                    CPU
                                </div>
                                <div class="collapse-content">
                                    <table class="table table-sm">
                                        <tbody>
                                            {#each Object.entries(systemData.资源使用情况.CPU) as [key, value]}
                                                <tr>
                                                    <td>{key}</td>
                                                    <td>{value}</td>
                                                </tr>
                                            {/each}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                            
                            <!-- 内存 -->
                            <div class="collapse collapse-arrow border border-base-300 bg-base-200 mt-2">
                                <input type="checkbox" checked />
                                <div class="collapse-title font-medium">
                                    内存
                                </div>
                                <div class="collapse-content">
                                    <table class="table table-sm">
                                        <tbody>
                                            {#each Object.entries(systemData.资源使用情况.内存) as [key, value]}
                                                <tr>
                                                    <td>{key}</td>
                                                    <td>{value}</td>
                                                </tr>
                                            {/each}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                            
                            <!-- 磁盘 -->
                            <div class="collapse collapse-arrow border border-base-300 bg-base-200 mt-2">
                                <input type="checkbox" checked />
                                <div class="collapse-title font-medium">
                                    磁盘
                                </div>
                                <div class="collapse-content">
                                    <table class="table table-sm">
                                        <tbody>
                                            {#each Object.entries(systemData.资源使用情况.磁盘) as [key, value]}
                                                <tr>
                                                    <td>{key}</td>
                                                    <td>{value}</td>
                                                </tr>
                                            {/each}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- 数据库状态 -->
                    <div class="card bg-base-100 shadow-xl">
                        <div class="card-body">
                            <h2 class="card-title">数据库状态</h2>
                            <div class="stats stats-vertical shadow-sm">
                                {#each Object.entries(systemData.数据库状态) as [key, value]}
                                    <div class="stat">
                                        <div class="stat-title">{key}</div>
                                        <div class="stat-value text-lg">
                                            {#if key === '连接状态'}
                                                <div class="badge {value === '已连接' ? 'badge-success' : 'badge-error'}">{value}</div>
                                            {:else}
                                                {value}
                                            {/if}
                                        </div>
                                    </div>
                                {/each}
                            </div>
                        </div>
                    </div>
                    
                    <!-- 应用配置 -->
                    <div class="card bg-base-100 shadow-xl md:col-span-2">
                        <div class="card-body">
                            <h2 class="card-title">应用配置</h2>
                            <div class="overflow-x-auto">
                                <table class="table table-zebra">
                                    <tbody>
                                        {#each Object.entries(systemData.应用配置) as [key, value]}
                                            <tr>
                                                <td class="font-medium">{key}</td>
                                                <td>{value.toString()}</td>
                                            </tr>
                                        {/each}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            {:else}
                <div class="alert alert-info">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current shrink-0 w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    <span>没有可显示的数据</span>
                </div>
            {/if}
        {/if}
    </div>
</div>
<script>
    import { onMount } from 'svelte';
    import axios from 'axios';
    import "$lib/style.css";
  
    // 状态变量
    let svelteKitInfo = {};
    let browserInfo = {};
    let networkStatus = { online: navigator.onLine };
    let performanceMetrics = {};
    let loading = true;
    let error = null;
    let lastUpdated = '';
    let networkTestInProgress = false;
  
    // 格式化字节数
    function formatBytes(bytes, decimals = 2) {
      if (bytes === 0) return '0 Bytes';
      const k = 1024;
      const dm = decimals < 0 ? 0 : decimals;
      const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
    }
  
    // 获取SvelteKit信息
    function getSvelteKitInfo() {
      return {
        '运行模式': import.meta.env.MODE || '未知',
        '开发环境': import.meta.env.DEV ? '是' : '否',
        '生产环境': import.meta.env.PROD ? '是' : '否',
        '服务端渲染': import.meta.env.SSR ? '启用' : '禁用',
        '浏览器环境': typeof window !== 'undefined' ? '是' : '否',
        '构建时间': import.meta.env.VITE_BUILD_TIME || '未知'
      };
    }
  
    // 修改 getBrowserInfo 函数
    function getBrowserInfo() {
      // 处理平台信息，使其更易理解
      let platformInfo = navigator.platform;
      if (platformInfo === 'Win32') {
        platformInfo = 'Windows 系统';
      } else if (platformInfo.includes('Linux')) {
        platformInfo = 'Linux 系统';
      } else if (platformInfo.includes('Mac')) {
        platformInfo = 'macOS 系统';
      }
      
      return {
        '用户代理': navigator.userAgent,
        '语言': navigator.language,
        '操作系统': platformInfo,
        '浏览器厂商': navigator.vendor || '未知',
        'Cookie启用': navigator.cookieEnabled ? '是' : '否',
        '禁止跟踪': navigator.doNotTrack ? '开启' : '关闭',
        '屏幕分辨率': `${window.screen.width}x${window.screen.height}`,
        '色彩深度': `${window.screen.colorDepth}位`,
        '时区': Intl.DateTimeFormat().resolvedOptions().timeZone,
        '暗色模式': window.matchMedia('(prefers-color-scheme: dark)').matches ? '是' : '否'
      };
    }
  
    // 获取性能指标
    function getPerformanceMetrics() {
      const perfData = window.performance;
      const navTiming = perfData.timing || {};
      
      const metrics = {
        '页面加载时间': '未知',
        'DOM加载完成': '未知',
        '首次绘制': '未知',
        '资源数量': perfData.getEntriesByType('resource').length
      };
      
      if (navTiming.loadEventEnd && navTiming.navigationStart) {
        metrics['页面加载时间'] = `${navTiming.loadEventEnd - navTiming.navigationStart}毫秒`;
      }
      
      if (navTiming.domContentLoadedEventEnd && navTiming.navigationStart) {
        metrics['DOM加载完成'] = `${navTiming.domContentLoadedEventEnd - navTiming.navigationStart}毫秒`;
      }
      
      const paintMetrics = perfData.getEntriesByType('paint');
      const firstPaint = paintMetrics.find(entry => entry.name === 'first-paint');
      if (firstPaint) {
        metrics['首次绘制'] = `${Math.round(firstPaint.startTime)}毫秒`;
      }
      
      return metrics;
    }
  
    // 检查网络状态
    async function checkNetworkStatus() {
      networkTestInProgress = true;
      
      try {
        // 使用当前域名进行测试，避免跨域问题
        const testUrl = window.location.origin;
        const startTime = Date.now();
        await axios.head(testUrl, { timeout: 5000 });
        const endTime = Date.now();
        
        networkTestInProgress = false;
        return {
          '在线状态': navigator.onLine ? '在线' : '离线',
          '网络延迟': `${endTime - startTime}毫秒`,
          '连接类型': navigator.connection ? navigator.connection.effectiveType : '未知',
          '下行速率': navigator.connection ? `${navigator.connection.downlink} Mbps` : '未知',
          '往返时延': navigator.connection ? `${navigator.connection.rtt}毫秒` : '未知'
        };
      } catch (err) {
        console.error('网络测试失败:', err);
        networkTestInProgress = false;
        return {
          '在线状态': navigator.onLine ? '在线' : '离线',
          '网络测试': '失败 - ' + (err.message || '未知错误'),
          '连接类型': navigator.connection ? navigator.connection.effectiveType : '未知',
          '下行速率': navigator.connection ? `${navigator.connection.downlink} Mbps` : '未知',
          '往返时延': navigator.connection ? `${navigator.connection.rtt}毫秒` : '未知'
        };
      }
    }
    
    // 重试网络测试
    async function retryNetworkTest() {
      try {
        networkStatus = await checkNetworkStatus();
        lastUpdated = new Date().toLocaleString();
      } catch (err) {
        console.error('重试网络测试失败:', err);
      }
    }
  
    // 刷新所有数据
    async function refreshData() {
      loading = true;
      error = null;
      
      try {
        svelteKitInfo = getSvelteKitInfo();
        browserInfo = getBrowserInfo();
        networkStatus = await checkNetworkStatus();
        performanceMetrics = getPerformanceMetrics();
        
        lastUpdated = new Date().toLocaleString();
      } catch (err) {
        error = `获取系统信息失败: ${err.message}`;
        console.error(error, err);
      } finally {
        loading = false;
      }
    }
  
    // 组件挂载时加载数据
    onMount(() => {
      refreshData();
      
      // 监听在线状态变化
      window.addEventListener('online', () => refreshData());
      window.addEventListener('offline', () => refreshData());
      
      return () => {
        window.removeEventListener('online', refreshData);
        window.removeEventListener('offline', refreshData);
      };
    });
</script>
  
<div class="container mx-auto px-4 py-6">
  <div class="flex justify-between items-center mb-6">
    <h1 class="text-2xl font-bold text-primary"><a href="/admin/user">前端服务监控</a></h1>
    
    <div class="flex items-center gap-4">
      {#if lastUpdated}
        <span class="text-sm text-gray-500">最后更新: {lastUpdated}</span>
      {/if}
      
      <button 
        on:click={refreshData}
        class="btn btn-primary btn-sm gap-2"
        disabled={loading}
      >
        {#if loading}
          <span class="loading loading-spinner loading-xs"></span>
          刷新中...
        {:else}
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          刷新数据
        {/if}
      </button>
    </div>
  </div>
  
  {#if loading && !lastUpdated}
    <div class="flex justify-center py-12">
      <span class="loading loading-spinner loading-lg text-primary"></span>
    </div>
  {:else if error}
    <div class="alert alert-error">
      <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
      <span>{error}</span>
    </div>
  {:else}
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <!-- SvelteKit 信息 -->
      <div class="card bg-base-100 shadow-xl">
        <div class="card-body">
          <h2 class="card-title flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-orange-500">
              <path d="M12 6h.01"></path>
              <path d="m19 6-3-3H8L5 6"></path>
              <path d="M5 6v12c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V6"></path>
            </svg>
            SvelteKit 环境
          </h2>
          <div class="divider my-1"></div>
          <div class="overflow-y-auto max-h-60">
            <table class="table table-zebra table-sm">
              <tbody>
                {#each Object.entries(svelteKitInfo) as [key, value]}
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
      
      <!-- 浏览器信息 -->
      <div class="card bg-base-100 shadow-xl">
        <div class="card-body">
          <h2 class="card-title flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-blue-500">
              <path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"></path>
              <path d="m7 15 5-5 5 5"></path>
              <path d="M12 10v7"></path>
            </svg>
            浏览器信息
          </h2>
          <div class="divider my-1"></div>
          <div class="overflow-y-auto max-h-60">
            <table class="table table-zebra table-sm">
              <tbody>
                {#each Object.entries(browserInfo) as [key, value]}
                  <tr>
                    <td class="font-medium">{key}</td>
                    <td class="text-sm break-all">{value}</td>
                  </tr>
                {/each}
              </tbody>
            </table>
          </div>
        </div>
      </div>
      
      <!-- 网络状态 -->
      <div class="card bg-base-100 shadow-xl">
        <div class="card-body">
          <h2 class="card-title flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-green-500">
              <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"></path>
            </svg>
            网络状态
          </h2>
          <div class="divider my-1"></div>
          <div class="overflow-y-auto max-h-60">
            <table class="table table-zebra table-sm">
              <tbody>
                <tr>
                  <td class="font-medium">在线状态</td>
                  <td>
                    <div class="badge {networkStatus['在线状态'] === '在线' ? 'badge-success' : 'badge-error'}">
                      {networkStatus['在线状态'] || (navigator.onLine ? '在线' : '离线')}
                    </div>
                  </td>
                </tr>
                {#each Object.entries(networkStatus).filter(([k]) => k !== '在线状态') as [key, value]}
                  <tr>
                    <td class="font-medium">{key}</td>
                    <td>{value}</td>
                  </tr>
                {/each}
              </tbody>
            </table>
            
            {#if networkStatus['网络测试'] && networkStatus['网络测试'].includes('失败')}
              <div class="mt-3">
                <button 
                  on:click={retryNetworkTest}
                  class="btn btn-outline btn-sm btn-warning w-full"
                  disabled={networkTestInProgress}
                >
                  {#if networkTestInProgress}
                    <span class="loading loading-spinner loading-xs"></span>
                    测试中...
                  {:else}
                    重新测试网络
                  {/if}
                </button>
              </div>
            {/if}
          </div>
        </div>
      </div>
      
      <!-- 性能指标 -->
      <div class="card bg-base-100 shadow-xl">
        <div class="card-body">
          <h2 class="card-title flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-purple-500">
              <path d="M12 2v4"></path>
              <path d="M12 18v4"></path>
              <path d="m4.93 4.93 2.83 2.83"></path>
              <path d="m16.24 16.24 2.83 2.83"></path>
              <path d="M2 12h4"></path>
              <path d="M18 12h4"></path>
              <path d="m4.93 19.07 2.83-2.83"></path>
              <path d="m16.24 7.76 2.83-2.83"></path>
            </svg>
            性能指标
          </h2>
          <div class="divider my-1"></div>
          <div class="overflow-y-auto max-h-60">
            <table class="table table-zebra table-sm">
              <tbody>
                {#each Object.entries(performanceMetrics) as [key, value]}
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
      
      <!-- 系统信息摘要卡片 -->
      <div class="card bg-base-100 shadow-xl">
        <div class="card-body">
          <h2 class="card-title flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-amber-500">
              <path d="M20 7h-3a2 2 0 0 1-2-2V2"></path>
              <path d="M16 2H8a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"></path>
              <path d="M12 13V7"></path>
              <path d="M15 10H9"></path>
            </svg>
            系统摘要
          </h2>
          <div class="divider my-1"></div>
          
          <div class="overflow-y-auto max-h-full">
            <div class="stats stats-vertical shadow w-full">
              <div class="stat">
                <div class="stat-figure text-primary">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect width="20" height="12" x="2" y="6" rx="2"></rect>
                    <path d="M12 12h.01"></path>
                    <path d="M17 12h.01"></path>
                    <path d="M7 12h.01"></path>
                  </svg>
                </div>
                <div class="stat-title">环境</div>
                <div class="stat-value text-lg">{svelteKitInfo['运行模式']}</div>
                <div class="stat-desc">{svelteKitInfo['开发环境'] === '是' ? '开发模式' : '生产模式'}</div>
              </div>
              
              <div class="stat">
                <div class="stat-figure text-secondary">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
                  </svg>
                </div>
                <div class="stat-title">资源数量</div>
                <div class="stat-value text-lg">{performanceMetrics['资源数量']}</div>
                <div class="stat-desc">页面加载的资源数</div>
              </div>
              
              <div class="stat">
                <div class="stat-figure text-info">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <polyline points="12 6 12 12 16 14"></polyline>
                  </svg>
                </div>
                <div class="stat-title">页面加载</div>
                <div class="stat-value text-lg">{performanceMetrics['页面加载时间'] !== '未知' ? performanceMetrics['页面加载时间'].replace('毫秒', '') : '0'}</div>
                <div class="stat-desc">毫秒</div>
              </div>
              

            </div>
          </div>
        </div>
      </div>
    </div>
  {/if}
</div>
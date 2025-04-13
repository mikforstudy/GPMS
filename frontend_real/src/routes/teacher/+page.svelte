<script>
  import { onMount } from 'svelte';
  import axios from 'axios';

  let username = $state('');

  
</script>

<!-- 主内容区域，分为上、中、下三层 -->
 <div  class="text-lg font-semibold mb-2 pl-3">教师</div>
<main class="flex-1 p-4 bg-white overflow-auto flex flex-col">
  <!-- 上层区域，垂直居中显示统计组件 -->
  <h2 class="text-lg font-semibold mb-2 pl-3">进度查看</h2>

  <section class="flex-1 border-b border-gray-300 pb-15 flex items-center justify-center">
    <!-- 统计组件 -->
    <div class="stats stats-vertical lg:stats-horizontal shadow">
      <div class="stat">
        <div class="stat-title">Downloads</div>
        <div class="stat-value">选题</div>
        <div class="stat-desc">Jan 1st - Feb 1st</div>
      </div>
      <div class="stat">
        <div class="stat-title">New Users</div>
        <div class="stat-value">开题</div>
        <div class="stat-desc">↗︎ 400 (22%)</div>
      </div>
      <div class="stat">
        <div class="stat-title">New Users</div>
        <div class="stat-value">中期</div>
        <div class="stat-desc">↗︎ 400 (22%)</div>
      </div>
      <div class="stat">
        <div class="stat-title">New Users</div>
        <div class="stat-value">论文</div>
        <div class="stat-desc">↗︎ 400 (22%)</div>
      </div>
      <div class="stat">
        <div class="stat-title">New Registers</div>
        <div class="stat-value">答辩</div>
        <div class="stat-desc">↘︎ 90 (14%)</div>
      </div>
    </div>
  </section>

  <!-- 中层区域 -->
  <section class="flex-2 border-b border-gray-300 p-4">
    <h2 class="text-lg font-semibold mb-2">中层内容</h2>
    <p>这里放置主要数据或操作面板。</p>
  </section>

  <!-- 下层区域 -->
  <section class="flex-1 p-2">
    <h2 class="text-lg font-semibold mb-2">下层内容</h2>
    <p>这里放置辅助信息或通知。</p>
  </section>
</main>
<script>
    import { onMount } from 'svelte';
  import '$lib/style.css';
  import axios from 'axios';

  let username = '';
  let projects = {};

  async function getData() {
    const res = await axios.get(`http://127.0.0.1:8000/api/v1/projects/student/${username}`);
    projects = res.data
    console.log(projects);
  }

  onMount(() => {
    if (typeof window !== 'undefined') {
      username = localStorage.getItem('username') || '用户';
      console.log(username);
    }
    getData();
  });
</script>

<!-- 主内容区域，分为上、中、下三层 -->
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

    <div>
      {#each projects as project}
        {project.title}--{project.description}--{project.status}--{new Date(project.start_date).toLocaleDateString()}
        --{project.teacher_name}
          <div class="flex justify-center gap-4">
    <div class="card w-48 bg-base-100 card-md shadow-sm">
      <div class="card-body">
        <h2 class="card-title">我的题目</h2>
        <p class="text-2xl">{project.title}</p>
        <div class="justify-end card-actions"></div>
      </div>
    </div>

<div class="card w-96 bg-base-100 card-md shadow-sm">
  <div class="card-body">
    <h2 class="card-title">详情</h2>
    <div class="break-words">{project.description}</div>
    <div class="justify-end card-actions"></div>
  </div>
</div>

        <div class="card w-48 bg-base-100 card-md shadow-sm">
      <div class="card-body">
        <h2 class="card-title">开始日期</h2>
        <!-- 使用 JavaScript 的 toLocaleDateString 方法来格式化日期，只显示年月日 -->
        <p>{new Date(project.start_date).toLocaleDateString()}</p>
          <h2 class="card-title">状态</h2>
        <p>{project.status}</p>
      </div>
    </div>
  </div>
      {/each}
    </div>
    <p>这里放置主要数据或操作面板。</p>
  </section>

  <!-- 下层区域 -->
  <section class="flex-1 p-2">
    <h2 class="text-lg font-semibold mb-2">下层内容</h2>
    <p>这里放置辅助信息或通知。</p>
  </section>
</main>
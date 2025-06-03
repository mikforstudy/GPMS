<script>
  import { onMount } from 'svelte';
  import '$lib/style.css';
  import axios from 'axios';

  let username = '';
  let projects = {};
  let phases = null; // 存储阶段时间数据
  let currentPhase = { name: '未知', start: null, end: null }; // 当前阶段信息
  const today = new Date(); // 用于在表格中高亮当前阶段

  async function getData() {
    const res = await axios.get(`http://127.0.0.1:8000/api/v1/projects/student/${username}`);
    projects = res.data;
    console.log(projects);
  }

  async function getPhaseData() {
    try {
      const res = await axios.get('http://127.0.0.1:8000/api/v1/phase/');
      phases = res.data;
      determineCurrentPhase();
    } catch (error) {
      console.error('获取阶段时间失败', error);
    }
  }

  function determineCurrentPhase() {
    if (!phases) return;
    
    const today = new Date();
    const phaseMap = [
      { name: '选题阶段', start: phases.time1_1, end: phases.time1_2 },
      { name: '开题阶段', start: phases.time2_1, end: phases.time2_2 },
      { name: '中期阶段', start: phases.time3_1, end: phases.time3_2 },
      { name: '论文阶段', start: phases.time4_1, end: phases.time4_2 },
      { name: '答辩阶段', start: phases.time5_1, end: phases.time5_2 }
    ];

    for (const phase of phaseMap) {
      const startDate = new Date(phase.start);
      const endDate = new Date(phase.end);
      
      if (today >= startDate && today <= endDate) {
        currentPhase = {
          name: phase.name,
          start: phase.start,
          end: phase.end
        };
        return;
      }
    }
    
    // 如果当前不在任何阶段内
    const firstPhaseStart = new Date(phases.time1_1);
    const lastPhaseEnd = new Date(phases.time5_2);
    
    if (today < firstPhaseStart) {
      currentPhase = { name: '毕设尚未开始', start: null, end: null };
    } else if (today > lastPhaseEnd) {
      currentPhase = { name: '毕设已结束', start: null, end: null };
    } else {
      // 在阶段之间的间隙，查找处于哪两个阶段之间
      for (let i = 0; i < phaseMap.length - 1; i++) {
        const currentEnd = new Date(phaseMap[i].end);
        const nextStart = new Date(phaseMap[i+1].start);
        
        if (today > currentEnd && today < nextStart) {
          currentPhase = { 
            name: `${phaseMap[i].name}已结束，准备${phaseMap[i+1].name}`, 
            start: phaseMap[i].end, 
            end: phaseMap[i+1].start
          };
          return;
        }
      }
    }
  }

  onMount(() => {
    if (typeof window !== 'undefined') {
      username = localStorage.getItem('username') || '用户';
      console.log(username);
    }
    getData();
    getPhaseData();
  });
</script>

<!-- 主内容区域，分为上、中、下三层 -->
<main class="flex-1 p-4 bg-white overflow-auto flex flex-col">
  <!-- 上层区域，垂直居中显示统计组件 -->
  <h2 class="text-lg font-semibold mb-2 pl-3">进度查看</h2>

  <section class="flex-1 border-b border-gray-300 pb-15 flex items-center justify-center">
    <!-- 统计组件 -->
    {#if phases}
      <div class="stats stats-vertical lg:stats-horizontal shadow">
        <div class="stat">
          <div class="stat-title">{phases.time1_1}</div>
          <div class="stat-value">选题</div>
          <div class="stat-desc">{phases.time1_2}</div>
        </div>
        <div class="stat">
          <div class="stat-title">{phases.time2_1}</div>
          <div class="stat-value">开题</div>
          <div class="stat-desc">{phases.time2_2}</div>
        </div>
        <div class="stat">
          <div class="stat-title">{phases.time3_1}</div>
          <div class="stat-value">中期</div>
          <div class="stat-desc">{phases.time3_2}</div>
        </div>
        <div class="stat">
          <div class="stat-title">{phases.time4_1}</div>
          <div class="stat-value">论文</div>
          <div class="stat-desc">{phases.time4_2}</div>
        </div>
        <div class="stat">
          <div class="stat-title">{phases.time5_1}</div>
          <div class="stat-value">答辩</div>
          <div class="stat-desc">{phases.time5_2}</div>
        </div>
      </div>
    {:else}
      <div class="flex justify-center items-center">
        <span class="loading loading-spinner loading-md"></span>
        <span class="ml-2">加载中...</span>
      </div>
    {/if}
  </section>

  <!-- 中层区域 -->
  <section class="flex-2 border-b border-gray-300 p-4">
    <h2 class="text-lg font-semibold mb-2">我的毕设项目</h2>

    <div>
      {#each Object.values(projects) as project}
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
    {#if !Object.keys(projects).length}
      <div class="flex justify-center items-center my-8">
        <p class="text-gray-500">暂无项目数据</p>
      </div>
    {/if}
  </section>

  <!-- 下层区域 -->
  <section class="flex-1 p-4">
    <h2 class="text-lg font-semibold mb-2">当前进度状态</h2>
    
    {#if phases}
      <div class="card bg-base-100 shadow-md">
        <div class="card-body">
          <div class="flex flex-wrap justify-between items-center mb-2 gap-4">
            <div>
              <div class="text-sm opacity-70">今日日期</div>
              <div class="font-bold">{new Date().toLocaleDateString()}</div>
            </div>
            <div>
              <div class="text-sm opacity-70">当前阶段</div>
              <div class="font-bold text-primary">{currentPhase.name}</div>
            </div>
            {#if currentPhase.start && currentPhase.end}
              <div>
                <div class="text-sm opacity-70">阶段时间</div>
                <div class="font-bold">{new Date(currentPhase.start).toLocaleDateString()} ~ {new Date(currentPhase.end).toLocaleDateString()}</div>
              </div>
            {/if}
          </div>
          
          <!-- 各阶段时间表 -->
          <div class="mt-4">
            <div class="text-sm font-semibold mb-2">全部阶段时间</div>
            <div class="overflow-x-auto">
              <table class="table table-xs table-zebra">
                <thead>
                  <tr>
                    <th>阶段</th>
                    <th>开始时间</th>
                    <th>结束时间</th>
                  </tr>
                </thead>
                <tbody>
                  <tr class={today >= new Date(phases.time1_1) && today <= new Date(phases.time1_2) ? 'bg-primary bg-opacity-20' : ''}>
                    <td>选题</td>
                    <td>{phases.time1_1}</td>
                    <td>{phases.time1_2}</td>
                  </tr>
                  <tr class={today >= new Date(phases.time2_1) && today <= new Date(phases.time2_2) ? 'bg-primary bg-opacity-20' : ''}>
                    <td>开题</td>
                    <td>{phases.time2_1}</td>
                    <td>{phases.time2_2}</td>
                  </tr>
                  <tr class={today >= new Date(phases.time3_1) && today <= new Date(phases.time3_2) ? 'bg-primary bg-opacity-20' : ''}>
                    <td>中期</td>
                    <td>{phases.time3_1}</td>
                    <td>{phases.time3_2}</td>
                  </tr>
                  <tr class={today >= new Date(phases.time4_1) && today <= new Date(phases.time4_2) ? 'bg-primary bg-opacity-20' : ''}>
                    <td>论文</td>
                    <td>{phases.time4_1}</td>
                    <td>{phases.time4_2}</td>
                  </tr>
                  <tr class={today >= new Date(phases.time5_1) && today <= new Date(phases.time5_2) ? 'bg-primary bg-opacity-20' : ''}>
                    <td>答辩</td>
                    <td>{phases.time5_1}</td>
                    <td>{phases.time5_2}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    {:else}
      <div class="flex justify-center items-center h-32">
        <span class="loading loading-spinner loading-md"></span>
        <span class="ml-2">加载阶段数据中...</span>
      </div>
    {/if}
  </section>
</main>
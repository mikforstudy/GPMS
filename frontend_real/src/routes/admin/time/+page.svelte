<script>
    import { onMount } from 'svelte';
    import axios from 'axios';
    
    // 阶段时间数据
    let phaseData = {
      time1_1: '',
      time1_2: '',
      time2_1: '',
      time2_2: '',
      time3_1: '',
      time3_2: '',
      time4_1: '',
      time4_2: '',
      time5_1: '',
      time5_2: ''
    };
  
    // 原始数据用于重置
    let originalData = { ...phaseData };
    
    // 加载状态
    let loading = false;
    let submitting = false;
    
    // 消息提示状态
    let message = '';
    let messageType = ''; // 'success' 或 'error'
    let showMessage = false;
    
    // 阶段名称映射
    const phaseNames = {
      time1_1: '选题开始时间',
      time1_2: '选题结束时间',
      time2_1: '开题开始时间',
      time2_2: '开题结束时间',
      time3_1: '中期开始时间',
      time3_2: '中期结束时间',
      time4_1: '论文开始时间',
      time4_2: '论文结束时间',
      time5_1: '答辩开始时间',
      time5_2: '答辩结束时间'
    };
  
    // 显示消息提示
    function showToast(msg, type = 'success') {
      message = msg;
      messageType = type;
      showMessage = true;
      
      // 3秒后自动关闭
      setTimeout(() => {
        showMessage = false;
      }, 3000);
    }
  
    // 获取当前阶段时间设置
    async function fetchPhaseData() {
      loading = true;
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/v1/phase/');
        phaseData = response.data;
        originalData = { ...phaseData };
        loading = false;
      } catch (error) {
        console.error('获取阶段时间失败', error);
        showToast('获取阶段时间失败，请刷新页面重试', 'error');
        loading = false;
      }
    }
  
    // 更新阶段时间设置
    async function updatePhaseData() {
      submitting = true;
      try {
        // 构建请求数据，排除id字段
        const requestData = { ...phaseData };
        delete requestData.id;
  
        // 发送更新请求
        const response = await axios.put(`http://127.0.0.1:8000/api/v1/phase/1`, requestData);
        
        if (response.data) {
          showToast('阶段时间更新成功');
          // 更新原始数据
          originalData = { ...phaseData };
        }
      } catch (error) {
        console.error('更新阶段时间失败', error);
        showToast('更新阶段时间失败，请重试', 'error');
      } finally {
        submitting = false;
      }
    }
  
    // 重置表单
    function resetForm() {
      phaseData = { ...originalData };
    }
  
    // 验证日期逻辑
    function validateDates() {
      // 检查所有的日期是否按顺序排列
      const dates = [
        new Date(phaseData.time1_1),
        new Date(phaseData.time1_2),
        new Date(phaseData.time2_1),
        new Date(phaseData.time2_2),
        new Date(phaseData.time3_1),
        new Date(phaseData.time3_2),
        new Date(phaseData.time4_1),
        new Date(phaseData.time4_2),
        new Date(phaseData.time5_1),
        new Date(phaseData.time5_2)
      ];
  
      for (let i = 0; i < dates.length - 1; i++) {
        if (dates[i] > dates[i + 1]) {
          return false;
        }
      }
      return true;
    }
  
    onMount(() => {
      fetchPhaseData();
    });
  </script>
  
  <div class="p-6 bg-white rounded-lg shadow-md">
    <h1 class="text-2xl font-bold mb-6 text-gray-800">毕业设计阶段时间管理</h1>
    
    <!-- 消息提示 -->
    {#if showMessage}
      <div class="toast toast-top toast-end z-50">
        <div class={`alert ${messageType === 'success' ? 'alert-success' : 'alert-error'}`}>
          <span>{message}</span>
        </div>
      </div>
    {/if}
    
    {#if loading}
      <div class="flex justify-center items-center p-10">
        <span class="loading loading-spinner loading-lg"></span>
        <span class="ml-3">正在加载数据...</span>
      </div>
    {:else}
      <form on:submit|preventDefault={updatePhaseData} class="space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- 阶段输入字段 -->
          {#each Object.entries(phaseNames) as [field, label]}
            <div class="form-control">
              <label class="label">
                <span class="label-text font-medium">{label}</span>
              </label>
              <input 
                type="date" 
                class="input input-bordered w-full" 
                bind:value={phaseData[field]}
                required
              />
            </div>
          {/each}
        </div>
  
        <!-- 时间轴可视化 -->
        <div class="mt-8 mb-4">
          <h2 class="text-lg font-semibold mb-2">阶段时间线</h2>
          <div class="w-full h-16 bg-gray-100 rounded-lg relative overflow-hidden">
            <!-- 各阶段图示 -->
            {#if phaseData.time1_1 && phaseData.time5_2}
              {@const startDate = new Date(phaseData.time1_1)}
              {@const endDate = new Date(phaseData.time5_2)}
              {@const totalDuration = endDate - startDate}
              
              <!-- 选题阶段 -->
              <div class="absolute h-full bg-blue-200 flex items-center justify-center text-xs"
                  style="left: {(new Date(phaseData.time1_1) - startDate) / totalDuration * 100}%; 
                         width: {(new Date(phaseData.time1_2) - new Date(phaseData.time1_1)) / totalDuration * 100}%;">
                选题
              </div>
              
              <!-- 开题阶段 -->
              <div class="absolute h-full bg-green-200 flex items-center justify-center text-xs"
                  style="left: {(new Date(phaseData.time2_1) - startDate) / totalDuration * 100}%; 
                         width: {(new Date(phaseData.time2_2) - new Date(phaseData.time2_1)) / totalDuration * 100}%;">
                开题
              </div>
              
              <!-- 中期阶段 -->
              <div class="absolute h-full bg-yellow-200 flex items-center justify-center text-xs"
                  style="left: {(new Date(phaseData.time3_1) - startDate) / totalDuration * 100}%; 
                         width: {(new Date(phaseData.time3_2) - new Date(phaseData.time3_1)) / totalDuration * 100}%;">
                中期
              </div>
              
              <!-- 论文阶段 -->
              <div class="absolute h-full bg-purple-200 flex items-center justify-center text-xs"
                  style="left: {(new Date(phaseData.time4_1) - startDate) / totalDuration * 100}%; 
                         width: {(new Date(phaseData.time4_2) - new Date(phaseData.time4_1)) / totalDuration * 100}%;">
                论文
              </div>
              
              <!-- 答辩阶段 -->
              <div class="absolute h-full bg-red-200 flex items-center justify-center text-xs"
                  style="left: {(new Date(phaseData.time5_1) - startDate) / totalDuration * 100}%; 
                         width: {(new Date(phaseData.time5_2) - new Date(phaseData.time5_1)) / totalDuration * 100}%;">
                答辩
              </div>
            {/if}
          </div>
        </div>
  
        <div class="flex justify-between mt-8">
          <button 
            type="button" 
            class="btn btn-outline" 
            on:click={resetForm}
            disabled={submitting}
          >
            重置
          </button>
          
          <button 
            type="submit" 
            class="btn btn-primary" 
            disabled={submitting || !validateDates()}
          >
            {#if submitting}
              <span class="loading loading-spinner loading-xs mr-2"></span>
            {/if}
            保存修改
          </button>
        </div>
  
        {#if !validateDates()}
          <div class="alert alert-warning mt-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
            <span>日期顺序有误，请确保每个阶段的开始时间早于结束时间，且各阶段按顺序排列</span>
          </div>
        {/if}
      </form>
  
      <!-- 表格显示 -->
      <div class="mt-10">
        <h2 class="text-lg font-semibold mb-2">当前阶段时间概览</h2>
        <div class="overflow-x-auto">
          <table class="table table-zebra">
            <thead>
              <tr>
                <th>阶段</th>
                <th>开始时间</th>
                <th>结束时间</th>
                <th>持续天数</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>选题阶段</td>
                <td>{phaseData.time1_1}</td>
                <td>{phaseData.time1_2}</td>
                <td>{Math.ceil((new Date(phaseData.time1_2) - new Date(phaseData.time1_1)) / (1000 * 60 * 60 * 24))}</td>
              </tr>
              <tr>
                <td>开题阶段</td>
                <td>{phaseData.time2_1}</td>
                <td>{phaseData.time2_2}</td>
                <td>{Math.ceil((new Date(phaseData.time2_2) - new Date(phaseData.time2_1)) / (1000 * 60 * 60 * 24))}</td>
              </tr>
              <tr>
                <td>中期阶段</td>
                <td>{phaseData.time3_1}</td>
                <td>{phaseData.time3_2}</td>
                <td>{Math.ceil((new Date(phaseData.time3_2) - new Date(phaseData.time3_1)) / (1000 * 60 * 60 * 24))}</td>
              </tr>
              <tr>
                <td>论文阶段</td>
                <td>{phaseData.time4_1}</td>
                <td>{phaseData.time4_2}</td>
                <td>{Math.ceil((new Date(phaseData.time4_2) - new Date(phaseData.time4_1)) / (1000 * 60 * 60 * 24))}</td>
              </tr>
              <tr>
                <td>答辩阶段</td>
                <td>{phaseData.time5_1}</td>
                <td>{phaseData.time5_2}</td>
                <td>{Math.ceil((new Date(phaseData.time5_2) - new Date(phaseData.time5_1)) / (1000 * 60 * 60 * 24))}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    {/if}
  </div>
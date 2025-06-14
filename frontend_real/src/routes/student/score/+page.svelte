<script>
  import { onMount } from "svelte";
  import axios from "axios";
  
  let username = '';
  let student_id = 0;
  let score = null;
  let loading = true;
  let error = null;
  let noScoreFound = false;  // 表示成绩不存在

  onMount(() => {
    if (typeof window !== 'undefined') {
      username = localStorage.getItem('username') || '用户';
      student_id = localStorage.getItem('student_id') || '0';
      fetchScore();
    }
  });

  async function fetchScore() {
    try {
      loading = true;
      // 使用新的API接口路径
      const response = await axios.get(`http://127.0.0.1:8000/api/v1/group/student/${student_id}/score`);
      score = response.data;
      loading = false;
    } catch (err) {
      console.error("获取成绩信息失败:", err);
      loading = false;
      
      // 检查是否是 404 错误（评分信息不存在）
      if (err.response && err.response.status === 404) {
        noScoreFound = true;
        error = null;  // 清除一般错误
      } else {
        // 其他类型的错误
        error = "获取成绩信息失败，请稍后重试";
        noScoreFound = false;
      }
    }
  }

  // 根据分数获取等级
  function getGradeFromScore(score) {
    if (score >= 90) return '优秀';
    if (score >= 80) return '良好';
    if (score >= 60) return '合格';
    return '不合格';
  }

  // 获取成绩对应的样式
  function getScoreStyle(grade) {
    switch(grade) {
      case '优秀':
        return 'text-emerald-500 bg-emerald-50';
      case '良好':
        return 'text-blue-500 bg-blue-50';
      case '合格':
        return 'text-amber-500 bg-amber-50';
      case '不合格':
        return 'text-red-500 bg-red-50';
      default:
        return 'text-gray-500 bg-gray-50';
    }
  }
  
  // 格式化日期
  function formatDate(dateString) {
    if (!dateString) return '未知日期';
    
    const date = new Date();
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  }
</script>

<div class="p-6 max-w-4xl mx-auto">
  <h1 class="text-2xl font-bold mb-8 text-center">成绩查询</h1>
  
  <!-- 加载状态 -->
  {#if loading}
    <div class="flex justify-center items-center h-64">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>
  <!-- 错误状态 -->
  {:else if error}
    <div class="bg-red-50 border-l-4 border-red-500 p-4 mb-6">
      <div class="flex">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
          </svg>
        </div>
        <div class="ml-3">
          <p class="text-sm text-red-700">{error}</p>
        </div>
      </div>
    </div>
  <!-- 没有成绩数据（404 情况）-->
  {:else if noScoreFound}
    <div class="bg-white shadow-md rounded-lg p-8 text-center">
      <svg class="h-16 w-16 text-amber-300 mx-auto mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
      <h2 class="text-xl font-medium text-gray-600 mb-2">成绩尚未发布</h2>
      <p class="text-gray-500">您的成绩信息暂未录入系统，请耐心等待教师评分。</p>
      <button class="mt-4 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors" on:click={fetchScore}>
        刷新查询
      </button>
    </div>
  <!-- 显示成绩 -->
  {:else if score}
    <div class="bg-white rounded-lg shadow-lg overflow-hidden">
      <!-- 成绩卡片顶部 -->
      <div class="bg-blue-600 text-white px-6 py-4">
        <h2 class="text-xl font-semibold">毕业论文（设计）成绩单</h2>
        <!-- <p class="text-blue-100 text-sm">成绩评定日期: {formatDate()}</p> -->
      </div>
      
      <!-- 成绩信息 -->
      <div class="p-6">
        <!-- 主要成绩展示 -->
        <div class="flex justify-between items-center mb-8 border-b border-gray-200 pb-6">
          <div>
            <p class="text-sm text-gray-600 mb-1">论文（设计）最终成绩</p>
            <div class="flex items-center">
              <span class="text-3xl font-bold mr-3">{score.score4}分</span>
              <span class={`px-3 py-1 text-sm rounded-full ${getScoreStyle(getGradeFromScore(score.score4))}`}>
                {getGradeFromScore(score.score4)}
              </span>
            </div>
          </div>
          <div>
            <div class="text-right">
              <p class="text-sm text-gray-600">学生姓名</p>
              <p class="font-medium text-lg">{score.student_name}</p>
            </div>
          </div>
        </div>
        
        <!-- 详细评分信息 -->
        <div class="mb-6">
          <h3 class="text-lg font-medium mb-4">评分详情</h3>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="bg-gray-50 p-4 rounded-lg">
              <div class="text-sm text-gray-500 mb-1">指导教师评分</div>
              <div class="text-xl font-semibold">{score.score1}<span class="text-sm text-gray-500 ml-1">分</span></div>
              <div class="mt-1 text-xs">{getGradeFromScore(score.score1)}</div>
            </div>
            
            <div class="bg-gray-50 p-4 rounded-lg">
              <div class="text-sm text-gray-500 mb-1">评阅教师评分</div>
              <div class="text-xl font-semibold">{score.score2}<span class="text-sm text-gray-500 ml-1">分</span></div>
              <div class="mt-1 text-xs">{getGradeFromScore(score.score2)}</div>
            </div>
            
            <div class="bg-gray-50 p-4 rounded-lg">
              <div class="text-sm text-gray-500 mb-1">答辩委员会评分</div>
              <div class="text-xl font-semibold">{score.score3}<span class="text-sm text-gray-500 ml-1">分</span></div>
              <div class="mt-1 text-xs">{getGradeFromScore(score.score3)}</div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 底部说明 -->
      <div class="bg-gray-50 px-6 py-4 border-t border-gray-200">
        <div class="flex items-start">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <p class="text-sm text-gray-600">成绩说明: 优秀(90-100分)、良好(80-89分)、合格(60-79分)、不合格(60分以下)</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 成绩详情卡片 -->
    <div class="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
      <!-- 指导教师评语卡片 -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h3 class="font-medium text-gray-900 mb-4 flex items-center">
          <svg class="h-5 w-5 text-blue-500 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M18 13V5a2 2 0 00-2-2H4a2 2 0 00-2 2v8a2 2 0 002 2h3l3 3 3-3h3a2 2 0 002-2zM5 7a1 1 0 011-1h8a1 1 0 110 2H6a1 1 0 01-1-1zm1 3a1 1 0 100 2h3a1 1 0 100-2H6z" clip-rule="evenodd" />
          </svg>
          指导教师评语
        </h3>
        <p class="text-gray-600 text-sm italic">
          "{score.content1 || '暂无评语'}"
        </p>
      </div>
      
      <!-- 评阅教师评语卡片 -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h3 class="font-medium text-gray-900 mb-4 flex items-center">
          <svg class="h-5 w-5 text-green-500 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
            <path fill-rule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clip-rule="evenodd" />
          </svg>
          评阅教师评语
        </h3>
        <p class="text-gray-600 text-sm italic">
          "{score.content2 || '暂无评语'}"
        </p>
      </div>
      
      <!-- 答辩委员会意见卡片 -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h3 class="font-medium text-gray-900 mb-4 flex items-center">
          <svg class="h-5 w-5 text-purple-500 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v1h8v-1zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-1a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v1h-3zM4.75 12.094A5.973 5.973 0 004 15v1H1v-1a3 3 0 013.75-2.906z" />
          </svg>
          答辩委员会意见
        </h3>
        <p class="text-gray-600 text-sm italic">
          "{score.content3 || '暂无评语'}"
        </p>
      </div>
    </div>
  {/if}
</div>
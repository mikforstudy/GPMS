<script>
  import { onMount } from "svelte";
  import axios from "axios";
  
  let username = '';
  let student_id = 0;
  let selectedFiles = [];
  let uploadedFiles = []; // 存储已上传成功的文件
  let message = "";
  let messageType = "info"; // 消息类型：info, success, error
  let dragActive = false; // 拖拽状态

  onMount(() => {
    if (typeof window !== 'undefined') {
      username = localStorage.getItem('username') || '用户';
      student_id = localStorage.getItem('student_id') || '0';
    }
    fetchFileList(); // 页面加载时获取已上传文件列表
  });

  // 获取已上传文件列表 - 更新为处理新的接口返回格式
  async function fetchFileList() {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/api/v1/process/list/${student_id}`);
      
      // 新的返回格式是数组，每个元素包含file_name、file_size和file_ctime
      uploadedFiles = response.data.map(file => {
        return {
          name: file.file_name,
          size: formatFileSize(file.file_size), // 使用后端提供的文件大小
          uploadTime: formatDate(file.file_ctime) // 使用后端提供的创建时间
        };
      });
    } catch (error) {
      console.error("获取文件列表失败:", error);
      message = "获取已上传文件列表失败";
      messageType = "error";
      
      // 如果是404错误（文件夹不存在），显示空列表而不是错误
      if (error.response && error.response.status === 404) {
        uploadedFiles = [];
        message = "";
      }
    }
  }

  // 格式化日期 - 将时间戳转换为可读格式
  function formatDate(timestamp) {
    const date = new Date(timestamp * 1000); // 时间戳通常是秒，需要转换为毫秒
    return date.toLocaleString();
  }

  // 其余代码保持不变...
  // 处理文件选择 - 添加到现有文件列表
  function handleFileChange(event) {
    const newFiles = Array.from(event.target.files);
    
    // 检查文件重复
    const existingFileNames = selectedFiles.map(file => file.name);
    const uniqueNewFiles = newFiles.filter(file => !existingFileNames.includes(file.name));
    
    // 将新文件添加到列表而不是替换
    selectedFiles = [...selectedFiles, ...uniqueNewFiles];
    
    // 重置文件输入框，允许选择相同的文件
    event.target.value = '';
  }

  // 处理文件拖拽
  function handleDragEnter(e) {
    e.preventDefault();
    e.stopPropagation();
    dragActive = true;
  }
  
  function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    dragActive = false;
  }
  
  function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    dragActive = true;
  }
  
  function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    dragActive = false;
    
    if (e.dataTransfer.files.length > 0) {
      const newFiles = Array.from(e.dataTransfer.files);
      
      // 检查文件重复
      const existingFileNames = selectedFiles.map(file => file.name);
      const uniqueNewFiles = newFiles.filter(file => !existingFileNames.includes(file.name));
      
      // 将新文件添加到列表
      selectedFiles = [...selectedFiles, ...uniqueNewFiles];
    }
  }

  // 清空已选择的所有文件
  function clearSelectedFiles() {
    selectedFiles = [];
  }

  // 移除已选择的单个文件
  function removeSelectedFile(fileToRemove) {
    selectedFiles = selectedFiles.filter(file => file !== fileToRemove);
  }
  
  // 删除已上传的文件
  async function deleteFile(fileName) {
    try {
      await axios.delete(`http://127.0.0.1:8000/api/v1/process/delete/${student_id}?file_name=${encodeURIComponent(fileName)}`);
      message = "文件删除成功";
      messageType = "success";
      
      // 从列表中移除被删除的文件
      uploadedFiles = uploadedFiles.filter(file => file.name !== fileName);
    } catch (error) {
      console.error("删除文件失败:", error);
      message = "删除文件失败，请稍后重试";
      messageType = "error";
    }
  }

  // 上传文件
  async function handleUpload() {
    if (selectedFiles.length === 0) {
      message = "请先选择文件";
      messageType = "error";
      return;
    }

    const formData = new FormData();
    selectedFiles.forEach(file => formData.append("files", file));

    try {
      const response = await axios.post(
        `http://127.0.0.1:8000/api/v1/process/upload/${student_id}`,
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );
      message = `上传成功：${response.data.message}`;
      messageType = "success";
      
      // 上传成功后刷新文件列表
      await fetchFileList();
      
      // 清空选择的文件
      selectedFiles = [];
    } catch (error) {
      console.error("Error uploading file:", error);
      message = "上传失败，请稍后重试";
      messageType = "error";
    }
  }

  // 格式化文件大小
  function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }
  
  // 获取文件图标
  function getFileIcon(fileName) {
    const extension = fileName.split('.').pop().toLowerCase();
    
    const iconMap = {
      pdf: "📄",
      doc: "📝",
      docx: "📝",
      xls: "📊",
      xlsx: "📊",
      ppt: "📑",
      pptx: "📑",
      jpg: "🖼️",
      jpeg: "🖼️",
      png: "🖼️",
      gif: "🖼️",
      zip: "🗜️",
      rar: "🗜️",
      txt: "📃",
    };
    
    return iconMap[extension] || "📁";
  }
</script>

<!-- HTML部分保持不变 -->
<div class="p-6 bg-gray-50 ">
  <h2 class="text-xl font-bold mb-6">过程文档上传</h2>
  
  <!-- 文件上传区域 -->
  <div 
    class="mb-6 border-2 {dragActive ? 'border-blue-400 bg-blue-50' : 'border-dashed border-gray-300 bg-white'} 
    rounded-lg p-8 text-center transition-all duration-200"
    on:dragenter={handleDragEnter}
    on:dragleave={handleDragLeave}
    on:dragover={handleDragOver}
    on:drop={handleDrop}
  >
    <input 
      type="file" 
      id="file-input" 
      class="hidden" 
      multiple 
      on:change={handleFileChange}
    />
    
    <label for="file-input" class="flex flex-col items-center justify-center cursor-pointer w-full h-full">
      <!-- 上传图标 -->
      <div class="w-16 h-16 mb-4 flex items-center justify-center rounded-full bg-gray-100">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
        </svg>
      </div>
      
      {#if selectedFiles.length > 0}
        <!-- 已选择文件的提示 -->
        <div class="mb-2 px-4 py-2 bg-blue-100 text-blue-800 rounded-full">
          已选择 <span class="font-bold">{selectedFiles.length}</span> 个文件
        </div>
        <p class="text-sm text-gray-600">点击添加更多文件或拖放文件到此处</p>
      {:else}
        <h3 class="text-lg font-medium text-gray-700">拖放文件到此处</h3>
        <p class="text-sm text-gray-600 mt-1">或点击选择文件</p>
        <p class="text-xs text-gray-500 mt-2">支持多文件同时上传</p>
      {/if}
    </label>
  </div>

  <!-- 已选择文件展示 -->
  {#if selectedFiles.length > 0}
    <div class="mb-6 bg-white rounded-lg shadow-sm overflow-hidden">
      <div class="bg-gray-50 px-4 py-3 border-b flex items-center justify-between">
        <h3 class="font-medium text-gray-700">已选择 {selectedFiles.length} 个文件</h3>
        <button 
          class="text-sm text-gray-500 hover:text-red-500"
          on:click={clearSelectedFiles}
        >
          清空所有
        </button>
      </div>
      
      <ul class="divide-y divide-gray-100 max-h-60 overflow-y-auto">
        {#each selectedFiles as file, i}
          <li class="flex items-center px-4 py-3 hover:bg-gray-50">
            <div class="text-2xl mr-3">{getFileIcon(file.name)}</div>
            <div class="flex-grow">
              <p class="font-medium text-gray-800 truncate">{file.name}</p>
              <p class="text-xs text-gray-500">{formatFileSize(file.size)}</p>
            </div>
            <button 
              class="ml-2 p-1 rounded-full hover:bg-gray-200 text-gray-500 hover:text-red-500 transition-colors"
              on:click={() => removeSelectedFile(file)}
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </button>
          </li>
        {/each}
      </ul>
      
      <div class="px-4 py-3 bg-gray-50 text-right">
        <button 
          class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
          on:click={handleUpload}
        >
          上传 {selectedFiles.length} 个文件
        </button>
      </div>
    </div>
  {:else}
    <button 
      class="btn btn-primary mb-6 w-full disabled:opacity-50" 
      disabled={true}
    >
      请先选择要上传的文件
    </button>
  {/if}

  <!-- 消息通知 -->
  {#if message}
    <div 
      class="mb-6 p-4 rounded-md {messageType === 'success' ? 'bg-green-50 text-green-800' : messageType === 'error' ? 'bg-red-50 text-red-800' : 'bg-blue-50 text-blue-800'}"
    >
      <div class="flex">
        <div class="flex-shrink-0">
          {#if messageType === 'success'}
            <svg class="h-5 w-5 text-green-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
            </svg>
          {:else if messageType === 'error'}
            <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
            </svg>
          {:else}
            <svg class="h-5 w-5 text-blue-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
            </svg>
          {/if}
        </div>
        <div class="ml-3">
          <p class="text-sm">{message}</p>
        </div>
      </div>
    </div>
  {/if}

  <!-- 已上传文件列表 -->
  {#if uploadedFiles.length > 0}
    <div class="bg-white rounded-lg shadow-sm overflow-hidden">
      <div class="bg-gray-50 px-4 py-3 border-b">
        <h3 class="font-medium text-gray-700">已上传文件 ({uploadedFiles.length})</h3>
      </div>
      
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">文件名</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">大小</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">上传时间</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            {#each uploadedFiles as file}
              <tr class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="text-2xl mr-3">{getFileIcon(file.name)}</div>
                    <div>
                      <div class="text-sm font-medium text-gray-900">{file.name}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{file.size}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{file.uploadTime}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  <button 
                    class="text-red-600 hover:text-red-900 focus:outline-none"
                    on:click={() => deleteFile(file.name)}
                  >
                    删除
                  </button>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </div>
  {:else}
    <div class="text-center py-8 text-gray-500">
      暂无已上传文件
    </div>
  {/if}
</div>
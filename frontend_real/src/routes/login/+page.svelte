<script>
  
  import axios from 'axios';
  import "$lib/style.css";


  const apiUrl = import.meta.env.VITE_API_URL;
  
  let student_id = 0;
  let username = '';
  let password = '';
  let userType = 'student';

  function handleSubmit() {
    console.log('用户名:', username);
    console.log('密码:', password);
    console.log('用户类型:', userType);

    axios.post(`${apiUrl}/api/v1/users/login`, {
      'username': username,
      'password': password,
      'userType': userType
    }, {
      headers: {
        'Content-Type': 'application/json',
        'accept': 'application/json'
      }
    })
    .then(response => {
      if (response.status === 200) {
        // 保存用户名到 localStorage
        localStorage.setItem('username', username);

        student_id = response.data.student_id;
        // 保存学生id到 localStorage
        localStorage.setItem('student_id', student_id);
       

        // 根据不同用户类型跳转不同界面
        if (userType === 'student') {
          window.location.href = '/student';
        } else if (userType === 'teacher') {
          window.location.href = '/teacher/notify';
        } else if (userType === 'admin') {
          window.location.href = '/admin';
        }
      } else {
        alert('登录失败，请检查用户名或密码');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('登录失败，请稍后重试');
    });
  }
</script>

<style>
  /* 背景图片样式示例，可根据需要修改 */
  .login-hero {
    background-image: url("img/【哲风壁纸】地平线-大海-帆船.png");/* 去掉 /static/，因为在Svelte中，static目录的内容被直接映射到根路径 */
    background-size: cover;
    background-position: center;
  }
  /* 给登录卡片增加 80% 透明度 */
  .card {
    background-color: rgba(255, 255, 255, 0.8);
  }
  /* 标题样式，保持原有样式 */
  .login-title {
    position: absolute;
    top: 20px;
    left: 20px;
    font-size: 24px;
    font-weight: bold;
    color: white;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  }
  /* 新增通知公告区域样式 */
  .notification-area {
    position: absolute;
    top: 70px;
    left: 20px;
    background-color: rgba(0, 0, 0, 0.5);
    color: white;
    padding: 10px;
    border-radius: 5px;
    font-size: 14px;
    max-width: 250px;
  }
  /* 输入框全宽 */
  .form-control {
    width: 100%;
  }
  /* 登录按钮设置为输入框80%宽度，并居中展示 */
  .btn {
    width: 80%;
    margin: 0 auto;
    display: block;
  }
</style>

<div class="hero min-h-screen login-hero">
  <!-- 添加标题 -->
  <div class="login-title">大学生毕业论文（设计）管理系统</div>
  <!-- 新增通知公告区域 -->
  <div class="notification-area">
    <h2 class="text-base font-bold mb-1">通知公告</h2>
    <ul class="list-disc list-inside">
      <li>公告1：系统维护预告。</li>
      <li>公告2：新功能上线。</li>
      <li>公告3：近期更新计划。</li>
    </ul>
  </div>
  <div class="hero-content flex-col md:flex-row items-center justify-end w-full px-8">
    <div class="w-full md:w-1/2 flex justify-end">
      <div class="card shadow-2xl bg-base-100 max-w-sm w-full">
        <div class="card-body">
          <h1 class="text-3xl font-bold mb-4">登录</h1>
          <!-- 用户类型下拉框 -->
          <div class="form-control">
            <label class="label">
              <span class="label-text">用户类型</span>
            </label>
            <select class="select select-bordered" bind:value={userType}>
              <option value="student">学生</option>
              <option value="teacher">教师</option>
              <option value="admin">管理员</option>
            </select>
          </div>
          <!-- 用户名输入框 -->
          <div class="form-control mt-4">
            <label class="label">
              <span class="label-text">用户名</span>
            </label>
            <input
              type="text"
              class="input input-bordered"
              placeholder="请输入用户名"
              bind:value={username}
            />
          </div>
          <!-- 密码输入框 -->
          <div class="form-control mt-4">
            <label class="label">
              <span class="label-text">密码</span>
            </label>
            <input
              type="password"
              class="input input-bordered"
              placeholder="请输入密码"
              bind:value={password}
            />
          </div>
          <!-- 登录按钮 -->
          <div class="form-control mt-6">
            <button class="btn btn-primary" on:click={handleSubmit}>
              登录
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
# Discord 學號註冊機器人

這是一個 Discord 機器人，允許用戶註冊他們的學號，並將他們分配到相應的身份組。機器人還可以檢查學號的組別，並提供相關的反饋。

## 功能

- **學號註冊**：用戶可以通過 `register` 指令註冊他們的學號。機器人會將用戶的學號和用戶名記錄到資料庫中，並將用戶分配到相應的身份組。
- **學號檢查**：用戶可以通過 `check` 指令檢查學號所屬的組別。
- **自動分配身份組**：根據學號的前綴，自動分配到對應的身份組。
- **錯誤處理**：處理註冊過程中的錯誤，並提供相應的反饋。
## 安装

1. **克隆仓库**：
   ```sh
   git clone https://github.com/TokdEd/discord-verification-bot.git
    ```
2. **創建虛擬環境**(可選,但推薦):
    ```sh
    python -m venv venv
    ```
3. **安裝依賴**：
    ```sh
    pip install -r requirements.txt
    ```

4. **創建 .env 文件：在項目根目錄下創建一個名為 .env 的文件，並添加以下內容：**
    ```sh
DISCORD_BOT_TOKEN=your-discord-bot-token
    ```
將 your-discord-bot-token 替換為你自己的 Discord 機器人令牌。

5. **初始化資料庫：運行以下命令以創建資料庫和表：**

    ```sh
    python setup_db.py
    ```

6. **啟動機器人：**

    ```sh
    python verify.py
    ```
## 使用指令：

    /register [學號]：註冊學號並分配到相應的身份組。例如：/register 1315689
    /check [學號]：檢查學號所屬的組別。例如：/check 2312005

## 日誌
    機器人的日誌將輸出到控制台，記錄了操作過程中的信息和錯誤。

## 貢獻
    歡迎提交問題和拉取請求。如果你發現任何錯誤或有改進建議，請創建一個 issue 或提交一個 pull request。

 ## 授權
    本專案採用' [MIT](/LICENSE)' 授權。

## 備註
    請確保你的機器人具有適當的權限，以便能夠管理角色和發送消息。
    確保角色的名稱與 assign_group 函數中的名稱匹配，以便機器人可以正確分配角色。


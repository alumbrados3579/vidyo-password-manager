using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Net.Http;
using System.ServiceModel;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Xml;

namespace VidyoPasswordManager
{
    public partial class MainForm : Form
    {
        private readonly string[] monthUsernames = {
            "jan", "feb", "mar", "apr", "may", "jun",
            "jul", "aug", "sep", "oct", "nov", "dec"
        };

        private ComboBox cmbUsername;
        private TextBox txtPassword;
        private TextBox txtPortalUrl;
        private TextBox txtAdminUser;
        private TextBox txtAdminPassword;
        private Button btnUpdatePassword;
        private Button btnBulkUpdate;
        private CheckedListBox clbUsers;
        private TextBox txtLog;
        private ProgressBar progressBar;

        public MainForm()
        {
            InitializeComponent();
            LoadMonthUsernames();
        }

        private void InitializeComponent()
        {
            this.Text = "Vidyo Password Manager";
            this.Size = new Size(600, 500);
            this.StartPosition = FormStartPosition.CenterScreen;

            // Portal Configuration Group
            var grpPortal = new GroupBox
            {
                Text = "Portal Configuration",
                Location = new Point(10, 10),
                Size = new Size(560, 120)
            };

            var lblPortalUrl = new Label { Text = "Portal URL:", Location = new Point(10, 25), Size = new Size(80, 20) };
            txtPortalUrl = new TextBox { Location = new Point(100, 22), Size = new Size(300, 20), Text = "http://your-vidyo-portal.com" };

            var lblAdminUser = new Label { Text = "Admin User:", Location = new Point(10, 50), Size = new Size(80, 20) };
            txtAdminUser = new TextBox { Location = new Point(100, 47), Size = new Size(150, 20) };

            var lblAdminPassword = new Label { Text = "Admin Pass:", Location = new Point(10, 75), Size = new Size(80, 20) };
            txtAdminPassword = new TextBox { Location = new Point(100, 72), Size = new Size(150, 20), UseSystemPasswordChar = true };

            grpPortal.Controls.AddRange(new Control[] { lblPortalUrl, txtPortalUrl, lblAdminUser, txtAdminUser, lblAdminPassword, txtAdminPassword });

            // Single User Update Group
            var grpSingle = new GroupBox
            {
                Text = "Single User Password Update",
                Location = new Point(10, 140),
                Size = new Size(280, 120)
            };

            var lblUsername = new Label { Text = "Username:", Location = new Point(10, 25), Size = new Size(70, 20) };
            cmbUsername = new ComboBox { Location = new Point(85, 22), Size = new Size(80, 20), DropDownStyle = ComboBoxStyle.DropDownList };

            var lblPassword = new Label { Text = "New Password:", Location = new Point(10, 50), Size = new Size(90, 20) };
            txtPassword = new TextBox { Location = new Point(105, 47), Size = new Size(150, 20), UseSystemPasswordChar = true };

            btnUpdatePassword = new Button { Text = "Update Password", Location = new Point(105, 80), Size = new Size(120, 30) };
            btnUpdatePassword.Click += BtnUpdatePassword_Click;

            grpSingle.Controls.AddRange(new Control[] { lblUsername, cmbUsername, lblPassword, txtPassword, btnUpdatePassword });

            // Bulk Update Group
            var grpBulk = new GroupBox
            {
                Text = "Bulk Password Update",
                Location = new Point(300, 140),
                Size = new Size(270, 120)
            };

            var lblBulkPassword = new Label { Text = "Password for all:", Location = new Point(10, 25), Size = new Size(90, 20) };
            var txtBulkPassword = new TextBox { Location = new Point(105, 22), Size = new Size(150, 20), UseSystemPasswordChar = true, Name = "txtBulkPassword" };

            clbUsers = new CheckedListBox { Location = new Point(10, 50), Size = new Size(150, 60) };
            
            btnBulkUpdate = new Button { Text = "Bulk Update", Location = new Point(170, 80), Size = new Size(90, 30) };
            btnBulkUpdate.Click += BtnBulkUpdate_Click;

            grpBulk.Controls.AddRange(new Control[] { lblBulkPassword, txtBulkPassword, clbUsers, btnBulkUpdate });

            // Progress and Log
            progressBar = new ProgressBar { Location = new Point(10, 270), Size = new Size(560, 20), Visible = false };

            var lblLog = new Label { Text = "Operation Log:", Location = new Point(10, 300), Size = new Size(100, 20) };
            txtLog = new TextBox 
            { 
                Location = new Point(10, 325), 
                Size = new Size(560, 120), 
                Multiline = true, 
                ScrollBars = ScrollBars.Vertical,
                ReadOnly = true
            };

            this.Controls.AddRange(new Control[] { grpPortal, grpSingle, grpBulk, progressBar, lblLog, txtLog });
        }

        private void LoadMonthUsernames()
        {
            cmbUsername.Items.AddRange(monthUsernames);
            clbUsers.Items.AddRange(monthUsernames);
        }

        private async void BtnUpdatePassword_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrEmpty(cmbUsername.Text) || string.IsNullOrEmpty(txtPassword.Text))
            {
                MessageBox.Show("Please select a username and enter a password.", "Validation Error");
                return;
            }

            await UpdateSinglePassword(cmbUsername.Text, txtPassword.Text);
        }

        private async void BtnBulkUpdate_Click(object sender, EventArgs e)
        {
            var selectedUsers = clbUsers.CheckedItems.Cast<string>().ToList();
            var bulkPasswordTextBox = this.Controls.Find("txtBulkPassword", true).FirstOrDefault() as TextBox;
            
            if (selectedUsers.Count == 0 || string.IsNullOrEmpty(bulkPasswordTextBox?.Text))
            {
                MessageBox.Show("Please select users and enter a password.", "Validation Error");
                return;
            }

            await UpdateMultiplePasswords(selectedUsers, bulkPasswordTextBox.Text);
        }

        private async Task UpdateSinglePassword(string username, string password)
        {
            try
            {
                LogMessage($"Starting password update for user: {username}");
                
                // TODO: Implement actual Vidyo API call
                var success = await CallVidyoUpdateMemberAPI(username, password);
                
                if (success)
                {
                    LogMessage($"✓ Password updated successfully for {username}");
                    txtPassword.Clear();
                }
                else
                {
                    LogMessage($"✗ Failed to update password for {username}");
                }
            }
            catch (Exception ex)
            {
                LogMessage($"✗ Error updating {username}: {ex.Message}");
            }
        }

        private async Task UpdateMultiplePasswords(List<string> usernames, string password)
        {
            progressBar.Visible = true;
            progressBar.Maximum = usernames.Count;
            progressBar.Value = 0;

            foreach (var username in usernames)
            {
                await UpdateSinglePassword(username, password);
                progressBar.Value++;
                Application.DoEvents(); // Keep UI responsive
            }

            progressBar.Visible = false;
            LogMessage($"Bulk update completed for {usernames.Count} users.");
        }

        private async Task<bool> CallVidyoUpdateMemberAPI(string username, string password)
        {
            // TODO: Implement actual SOAP call to Vidyo API
            // This is a placeholder - you'll need to add service reference to Vidyo WSDL
            
            await Task.Delay(1000); // Simulate API call
            
            // Example of what the actual implementation would look like:
            /*
            try
            {
                var client = new VidyoPortalAdminServiceClient();
                client.ClientCredentials.UserName.UserName = txtAdminUser.Text;
                client.ClientCredentials.UserName.Password = txtAdminPassword.Text;
                
                // Get member first
                var member = await client.GetMemberAsync(username);
                
                // Update password
                member.password = password;
                var result = await client.UpdateMemberAsync(member.memberID, member);
                
                return result.Equals("OK");
            }
            catch (Exception ex)
            {
                LogMessage($"API Error: {ex.Message}");
                return false;
            }
            */
            
            return true; // Placeholder return
        }

        private void LogMessage(string message)
        {
            var timestamp = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");
            txtLog.AppendText($"[{timestamp}] {message}\r\n");
            txtLog.ScrollToCaret();
        }
    }

    // Program entry point
    public static class Program
    {
        [STAThread]
        public static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new MainForm());
        }
    }
}
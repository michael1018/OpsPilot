<template>
  <div>
    <!-- Top toolbar -->
    <div class="toolbar">
      <Button type="primary" @click="openAddModal">
        <Icon type="plus" /> Add User
      </Button>
      <Input
        v-model="searchValue"
        placeholder="Search..."
        class="search-input"
        @keyup.enter="handleSearch"
      />
      <Button type="primary" @click="handleSearch">
        <Icon type="search" /> Search
      </Button>
    </div>

    <!-- Users table -->
    <Tables
      :value="users"
      :columns="columns"
      :editable="true"
      :searchable="false"
      :height="500"
      @on-save-edit="handleSaveEdit"
    />

    <!-- Add/Edit modal -->
    <Modal
      v-model="modalVisible"
      :title="modalTitle"
      @on-ok="handleModalOk"
      @on-cancel="handleModalCancel"
    >
      <Form :model="modalForm">
        <FormItem label="Name">
          <Input v-model="modalForm.name" />
        </FormItem>

        <!-- Only show password on add -->
        <FormItem v-if="modalMode === 'add'" label="Password">
          <Input type="password" v-model="modalForm.password" />
        </FormItem>

        <FormItem label="Age">
          <Input type="number" v-model.number="modalForm.age" />
        </FormItem>

        <FormItem label="Sex">
          <Select v-model="modalForm.sex">
            <Option :value="1">Male</Option>
            <Option :value="2">Female</Option>
          </Select>
        </FormItem>

        <FormItem label="Status">
          <Select v-model="modalForm.status_code">
            <Option value="ACTIVE">Active</Option>
            <Option value="INACTIVE">Inactive</Option>
          </Select>
        </FormItem>

        <FormItem label="Birthdate">
          <DatePicker v-model="modalForm.birthdate" type="date" placeholder="Select birthdate" />
        </FormItem>
      </Form>
    </Modal>
  </div>
</template>

<script>
import Tables from "@/components/tables/tables.vue";
import { getUsersPages, createUser, updateUser, deleteUser } from "@/api/users-api";

export default {
  name: "Users",
  components: { Tables },
  data() {
    return {
      users: [],
      searchValue: "",
      columns: [
        { title: "ID", key: "id" },
        { title: "Name", key: "name", editable: false },
        { title: "Age", key: "age", editable: false },
        { title: "Birthdate", key: "birthdate", editable: false },
        {
          title: "Sex",
          key: "sex",
          editable: false,
          render: (h, { row }) => h("span", Number(row.sex) === 1 ? "Male" : "Female"),
        },
        {
          title: "Actions",
          key: "handle",
          button: [
            (h, params) =>
              h(
                "Button",
                {
                  props: { type: "primary", size: "small" },
                  on: { click: () => this.openEditModal(params.row) },
                  style: { marginRight: "5px" },
                },
                "Edit"
              ),
            (h, params) =>
              h(
                "Button",
                {
                  props: { type: "error", size: "small" },
                  on: { click: () => this.handleDelete(params.row) },
                },
                "Delete"
              ),
          ],
        },
      ],
      // Modal
      modalVisible: false,
      modalTitle: "",
      modalForm: {},
      modalMode: "add",
      searchKey: "name",
    };
  },
  created() {
    this.fetchUsers();
  },
  methods: {
    async fetchUsers() {
      const data = await getUsersPages(0, 10);
      this.users = data.list || data;
    },

    handleSearch() {
      if (!this.searchValue) {
        this.fetchUsers();
      } else {
        const key = this.searchKey || "name";
        this.users = this.users.filter(u => {
          const value = u[key] !== null && u[key] !== undefined ? u[key] : "";
          return String(value).includes(this.searchValue);
        });
      }
    },

    openAddModal() {
      this.modalMode = "add";
      this.modalTitle = "Add User";
      this.modalForm = {
        name: "",
        password: "",
        age: null,
        sex: 1,
        status_code: "ACTIVE",
        birthdate: null,
      };
      this.modalVisible = true;
    },

    openEditModal(row) {
      this.modalMode = "edit";
      this.modalTitle = "Edit User";
      this.modalForm = { ...row };
      delete this.modalForm.password; // don't send password on edit
      this.modalVisible = true;
    },

    handleModalCancel() {
      this.modalVisible = false;
    },

    async handleModalOk() {
      try {
        if (this.modalMode === "add") {
          const newUser = await createUser(this.modalForm);
          this.users.push(newUser);
          this.$Message.success("User created successfully");
        } else if (this.modalMode === "edit") {
          const { password, ...updateData } = this.modalForm; // exclude password
          const updatedUser = await updateUser(updateData);
          const idx = this.users.findIndex((u) => u.id === updatedUser.id);
          if (idx > -1) this.$set(this.users, idx, updatedUser);
          this.$Message.success("User updated successfully");
        }
        this.modalVisible = false;
      } catch (err) {
        let message = "Operation failed";
        // 改成傳統判斷
        if (err && err.response && err.response.data) {
          if (err.response.data.detail) {
            message = err.response.data.detail;
          } else if (err.response.data.message) {
            message = err.response.data.message;
          }
        }
        this.$Message.error(message);
      }
    },

    async handleSaveEdit({ row, column, value }) {
      const updatedRow = { ...row, [column.key]: value };
      const { password, ...updateData } = updatedRow;
      const updatedUser = await updateUser(updateData);
      const idx = this.users.findIndex((u) => u.id === updatedUser.id);
      if (idx > -1) this.$set(this.users, idx, updatedUser);
    },

    async handleDelete(row) {
      if (!confirm(`Delete user ${row.name}?`)) return;
      await deleteUser(row.id);
      this.users = this.users.filter((u) => u.id !== row.id);
      this.$Message.success("User deleted successfully");
    },
  },
};
</script>

<style scoped>
.toolbar {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}
.search-input {
  margin-left: 10px;
  width: 200px;
}
</style>

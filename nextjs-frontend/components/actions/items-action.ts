"use server";

// 读取 Cookie（拿 accessToken）。
import { cookies } from "next/headers";
// 自动生成的 Item 接口函数（查、删、增）。
import { readItem, deleteItem, createItem } from "@/app/clientService";
// 触发某个路径重新获取最新数据（Next.js 缓存失效）。
import { revalidatePath } from "next/cache";
// 用于创建成功后跳转。
import { redirect } from "next/navigation";
// Item 表单校验规则。
import { itemSchema } from "@/lib/definitions";

// 获取当前用户的 Item 列表（支持分页）。
export async function fetchItems(page: number = 1, size: number = 10) {
  // 读取 cookie 存储对象。
  const cookieStore = await cookies();
  // 取出 accessToken 字段。
  const token = cookieStore.get("accessToken")?.value;

  // 没有 token 直接返回错误信息。
  if (!token) {
    return { message: "No access token found" };
  }

  // 调用后端分页接口。
  const { data, error } = await readItem({
    query: {
      page: page,
      size: size,
    },
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  // 后端返回错误时，透传错误对象。
  if (error) {
    return { message: error };
  }

  // 正常返回分页数据。
  return data;
}

// 删除指定 Item。
export async function removeItem(id: string) {
  // 读取 cookie。
  const cookieStore = await cookies();
  // 提取 accessToken。
  const token = cookieStore.get("accessToken")?.value;

  // 未登录时返回提示。
  if (!token) {
    return { message: "No access token found" };
  }

  // 调用删除接口（路径参数 item_id）。
  const { error } = await deleteItem({
    headers: {
      Authorization: `Bearer ${token}`,
    },
    path: {
      item_id: id,
    },
  });

  // 删除失败时返回错误信息。
  if (error) {
    return { message: error };
  }
  // 删除成功后让 dashboard 页面缓存失效并刷新数据。
  revalidatePath("/dashboard");
}

// 创建新 Item（由新增表单触发）。
export async function addItem(prevState: {}, formData: FormData) {
  // 读取 cookie。
  const cookieStore = await cookies();
  // 提取 accessToken。
  const token = cookieStore.get("accessToken")?.value;

  // 未登录则无法创建。
  if (!token) {
    return { message: "No access token found" };
  }

  // 校验并转换表单输入（quantity 会从 string 转成 number）。
  const validatedFields = itemSchema.safeParse({
    name: formData.get("name"),
    description: formData.get("description"),
    quantity: formData.get("quantity"),
  });

  // 校验失败时返回字段错误。
  if (!validatedFields.success) {
    return { errors: validatedFields.error.flatten().fieldErrors };
  }

  // 取出合法数据。
  const { name, description, quantity } = validatedFields.data;

  // 组织创建接口参数。
  const input = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: {
      name,
      description,
      quantity,
    },
  };
  // 调用创建接口。
  const { error } = await createItem(input);
  // 后端失败时返回错误详情。
  if (error) {
    return { message: `${error.detail}` };
  }
  // 创建成功后跳回仪表盘。
  redirect(`/dashboard`);
}

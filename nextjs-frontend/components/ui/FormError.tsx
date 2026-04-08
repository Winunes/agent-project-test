// 统一定义 Action 返回的错误状态结构。
interface ErrorState {
  // 字段级错误（key 是字段名，value 可以是单条或多条错误）。
  errors?: {
    [key: string]: string | string[];
  };
  // 后端业务校验错误（例如账号密码错误）。
  server_validation_error?: string;
  // 其他服务端异常错误。
  server_error?: string;
}

// FormError 组件的属性定义。
interface FormErrorProps {
  // 表单状态对象（可选）。
  state?: ErrorState;
  // 额外 className（可选）。
  className?: string;
}

// 展示“表单级”错误（不对应具体字段）。
export function FormError({ state, className = "" }: FormErrorProps) {
  // 没有状态就不渲染任何内容。
  if (!state) return null;

  // 优先显示业务校验错误，否则显示通用服务端错误。
  const error = state.server_validation_error || state.server_error;
  // 没有错误时不渲染。
  if (!error) return null;

  // 渲染错误文本。
  return <p className={`text-sm text-red-500 ${className}`}>{error}</p>;
}

// FieldError 组件的属性定义。
interface FieldErrorProps {
  // 表单状态对象（可选）。
  state?: ErrorState;
  // 要显示错误的字段名（必填）。
  field: string;
  // 额外 className（可选）。
  className?: string;
}

// 展示“字段级”错误（例如 email/password 对应错误）。
export function FieldError({ state, field, className = "" }: FieldErrorProps) {
  // 没有字段错误集合时不渲染。
  if (!state?.errors) return null;

  // 取出目标字段错误。
  const error = state.errors[field];
  // 字段没有错误时不渲染。
  if (!error) return null;

  // 如果是多条错误，使用列表展示。
  if (Array.isArray(error)) {
    return (
      <div className={`text-sm text-red-500 ${className}`}>
        <ul className="list-disc ml-4">
          {error.map((err) => (
            <li key={err}>{err}</li>
          ))}
        </ul>
      </div>
    );
  }

  // 单条错误时直接用一行文本展示。
  return <p className={`text-sm text-red-500 ${className}`}>{error}</p>;
}

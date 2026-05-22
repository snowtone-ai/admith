interface Column<T> {
  key: string;
  header: string;
  numeric?: boolean;
  render?: (row: T) => React.ReactNode;
}

interface TableProps<T> {
  columns: Column<T>[];
  data: T[];
  keyField: keyof T;
}

export function Table<T>({ columns, data, keyField }: TableProps<T>) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse">
        <thead>
          <tr>
            {columns.map((col) => (
              <th
                key={col.key}
                className={[
                  "sticky top-0 bg-surface-1 px-4 py-3",
                  "font-mono text-[11px] font-medium uppercase tracking-wider text-ink-subtle",
                  col.numeric ? "text-right" : "text-left",
                ].join(" ")}
              >
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row) => (
            <tr
              key={String(row[keyField])}
              className="border-b border-hairline hoverable hover:bg-surface-1"
            >
              {columns.map((col) => (
                <td
                  key={col.key}
                  className={[
                    "px-4 py-3 text-[13px]",
                    col.numeric ? "text-right font-mono tabular-nums" : "",
                  ].join(" ")}
                >
                  {col.render ? col.render(row) : String((row as Record<string, unknown>)[col.key] ?? "")}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

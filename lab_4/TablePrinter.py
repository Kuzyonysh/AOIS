class TablePrinter:
    def print_table(self, hash_table):
        headers = ["Idx", "ID", "V", "h", "C", "U", "D", "Pi"]
        print(" | ".join(f"{h:<10}" for h in headers))
        print("-" * 80)

        for i, entry in enumerate(hash_table.table):

            if entry is None:
                print(f"{i:<10} | пусто")
                continue

            if entry.deleted:
                print(
                    f"{i:<10} | "
                    f"[DELETED]  | "
                    f"{'':<10} | "
                    f"{'':<10} | "
                    f"{entry.C:<10} | "
                    f"{entry.U:<10} | "
                    f"{entry.D:<10} | "
                    f"{''}"
                )
                continue

            V = hash_table.utils.get_vlue(entry.key)
            h = hash_table.utils.hash(entry.key)

            print(
                f"{i:<10} | "
                f"{entry.key:<10} | "
                f"{V:<10} | "
                f"{h:<10} | "
                f"{entry.C:<10} | "
                f"{entry.U:<10} | "
                f"{entry.D:<10} | "
                f"{entry.value}"
            )

        print("-" * 80)
        print(f"Коэффициент заполнения: {hash_table.load_factor():.2f}")